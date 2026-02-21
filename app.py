"""
Main Flask application for DEV Mobile & Services
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timedelta
import uuid

from config import config
from models import (
    db, User, Product, CartItem, Order, OrderItem, Category, Brand,
    Service, ServiceBooking, Review, ServiceReview, Wishlist, Address,
    Coupon, ContactMessage, ProductImage
)

# Create Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')

# Configuration
config_name = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[config_name])

# Initialize extensions
db.init_app(app)
CORS(app)

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


# ==================== AUTHENTICATION ROUTES ====================
@app.route('/auth/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        # Validate input
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        confirm_password = data.get('confirm_password', '')
        
        if not all([username, email, password, confirm_password]):
            return jsonify({'error': 'All fields are required'}), 400
        
        if password != confirm_password:
            return jsonify({'error': 'Passwords do not match'}), 400
        
        # Check if user exists
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already exists'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already exists'}), 400
        
        # Create new user
        try:
            user = User(
                username=username,
                email=email,
                first_name=data.get('first_name', ''),
                last_name=data.get('last_name', ''),
                phone=data.get('phone', '')
            )
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            session['user_id'] = user.id
            session['username'] = user.username
            session.permanent = True
            
            return jsonify({'message': 'Registration successful', 'user_id': user.id}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    
    return render_template('auth/register.html')


@app.route('/auth/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if request.method == 'POST':
        data = request.get_json() if request.is_json else request.form
        
        username_or_email = data.get('username_or_email', '').strip()
        password = data.get('password', '')
        
        if not username_or_email or not password:
            return jsonify({'error': 'Username/Email and password are required'}), 400
        
        # Find user by username or email
        user = User.query.filter(
            (User.username == username_or_email) | (User.email == username_or_email)
        ).first()
        
        if not user or not user.check_password(password):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Account is inactive'}), 401
        
        session['user_id'] = user.id
        session['username'] = user.username
        session['is_admin'] = user.is_admin
        session.permanent = True
        
        redirect_to = url_for('admin_dashboard' if user.is_admin else 'index')
        return jsonify({'message': 'Login successful', 'redirect': redirect_to}), 200
    
    return render_template('auth/login.html')


@app.route('/auth/logout')
def logout():
    """User logout"""
    session.clear()
    return redirect(url_for('index'))


# ==================== HOME & PRODUCT ROUTES ====================
@app.route('/')
@app.route('/home')
def index():
    """Homepage"""
    try:
        # Get featured products
        featured_products = Product.query.filter_by(is_active=True).limit(8).all()
        
        # Get trending products
        trending_products = Product.query.filter_by(is_active=True, is_trending=True).limit(4).all()
        
        # Get limited stock products
        limited_products = Product.query.filter_by(is_active=True, is_limited=True).limit(6).all()
        
        # Get categories for navigation
        categories = Category.query.filter_by(is_active=True).all()
        
        # Get brands
        brands = Brand.query.filter_by(is_active=True).all()
        
        return render_template('index.html',
                             featured_products=featured_products,
                             trending_products=trending_products,
                             limited_products=limited_products,
                             categories=categories,
                             brands=brands)
    except Exception as e:
        print(f"Error in index: {e}")
        return render_template('error.html', error='Unable to load homepage'), 500


@app.route('/products')
def products():
    """Product listing page"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    brand = request.args.get('brand', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    search = request.args.get('search', '')
    sort = request.args.get('sort', 'popular')  # popular, newest, price_low, price_high
    
    query = Product.query.filter_by(is_active=True)
    
    # Apply filters
    if category:
        category_obj = Category.query.filter_by(slug=category).first()
        if category_obj:
            query = query.filter_by(category_id=category_obj.id)
    
    if brand:
        brand_obj = Brand.query.filter_by(slug=brand).first()
        if brand_obj:
            query = query.filter_by(brand_id=brand_obj.id)
    
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))
    
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    
    # Apply sorting
    if sort == 'newest':
        query = query.order_by(Product.created_at.desc())
    elif sort == 'price_low':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_high':
        query = query.order_by(Product.price.desc())
    else:  # popular
        query = query.order_by(Product.rating.desc(), Product.review_count.desc())
    
    # Paginate
    paginated = query.paginate(page=page, per_page=12, error_out=False)
    
    return render_template('products.html',
                         products=paginated.items,
                         total_pages=paginated.pages,
                         current_page=page,
                         total_items=paginated.total)


@app.route('/product/<slug>')
def product_detail(slug):
    """Product detail page"""
    product = Product.query.filter_by(slug=slug).first_or_404()
    
    # Get related products
    related_products = Product.query.filter_by(
        category_id=product.category_id,
        is_active=True
    ).filter(Product.id != product.id).limit(4).all()
    
    # Get reviews
    reviews = Review.query.filter_by(product_id=product.id).all()
    
    # Check if user has this in wishlist
    in_wishlist = False
    if 'user_id' in session:
        in_wishlist = Wishlist.query.filter_by(
            user_id=session['user_id'],
            product_id=product.id
        ).first() is not None
    
    return render_template('product_detail.html',
                         product=product,
                         related_products=related_products,
                         reviews=reviews,
                         in_wishlist=in_wishlist)


# ==================== SHOPPING CART &  CHECKOUT ====================
@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    """Add product to cart"""
    if 'user_id' not in session:
        return jsonify({'error': 'Please login first'}), 401
    
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)
    
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    if product.stock_quantity < quantity:
        return jsonify({'error': 'Insufficient stock'}), 400
    
    cart_item = CartItem.query.filter_by(
        user_id=session['user_id'],
        product_id=product_id
    ).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(
            user_id=session['user_id'],
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(cart_item)
    
    db.session.commit()
    return jsonify({'message': 'Product added to cart'}), 201


@app.route('/api/cart/remove', methods=['POST'])
def remove_from_cart():
    """Remove product from cart"""
    if 'user_id' not in session:
        return jsonify({'error': 'Please login first'}), 401
    
    data = request.get_json()
    product_id = data.get('product_id')
    
    CartItem.query.filter_by(
        user_id=session['user_id'],
        product_id=product_id
    ).delete()
    
    db.session.commit()
    return jsonify({'message': 'Product removed from cart'}), 200


@app.route('/cart')
def view_cart():
    """View shopping cart"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    cart_items = CartItem.query.filter_by(user_id=session['user_id']).all()
    
    subtotal = sum(item.total_price for item in cart_items)
    tax = subtotal * 0.18  # 18% GST
    shipping = 50 if subtotal > 0 else 0
    total = subtotal + tax + shipping
    
    return render_template('cart.html',
                         cart_items=cart_items,
                         subtotal=subtotal,
                         tax=tax,
                         shipping=shipping,
                         total=total)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """Checkout page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    cart_items = CartItem.query.filter_by(user_id=session['user_id']).all()
    
    if not cart_items:
        return redirect(url_for('view_cart'))
    
    if request.method == 'POST':
        data = request.form
        
        # Create address
        address = Address(
            user_id=session['user_id'],
            street=data.get('street'),
            city=data.get('city'),
            state=data.get('state'),
            postal_code=data.get('postal_code'),
            phone=data.get('phone'),
            address_type='delivery'
        )
        db.session.add(address)
        db.session.commit()
        
        # Calculate totals
        subtotal = sum(item.total_price for item in cart_items)
        tax = subtotal * 0.18
        shipping = 50
        coupon_discount = 0
        
        # Apply coupon if provided
        coupon_code = data.get('coupon_code')
        if coupon_code:
            coupon = Coupon.query.filter_by(code=coupon_code).first()
            if coupon and coupon.is_valid():
                if coupon.discount_type == 'percent':
                    coupon_discount = (subtotal * coupon.discount_value) / 100
                else:
                    coupon_discount = coupon.discount_value
        
        total = subtotal + tax + shipping - coupon_discount
        
        # Create order
        order = Order(
            order_number=f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6].upper()}",
            user_id=session['user_id'],
            subtotal=subtotal,
            tax=tax,
            shipping=shipping,
            discount=coupon_discount,
            total_amount=total,
            payment_method=data.get('payment_method'),
            delivery_address=f"{address.street}, {address.city}, {address.state} {address.postal_code}"
        )
        
        # Add order items
        for cart_item in cart_items:
            order_item = OrderItem(
                order=order,
                product_id=cart_item.product_id,
                quantity=cart_item.quantity,
                price=cart_item.product.discounted_price,
                discount_amount=cart_item.product.savings * cart_item.quantity
            )
            db.session.add(order_item)
            
            # Update product stock
            cart_item.product.stock_quantity -= cart_item.quantity
        
        db.session.add(order)
        db.session.commit()
        
        # Clear cart
        CartItem.query.filter_by(user_id=session['user_id']).delete()
        db.session.commit()
        
        return redirect(url_for('order_confirmation', order_id=order.id))
    
    # Calculate cart totals
    subtotal = sum(item.total_price for item in cart_items)
    tax = subtotal * 0.18
    shipping = 50
    total = subtotal + tax + shipping
    
    user_addresses = Address.query.filter_by(user_id=session['user_id']).all()
    
    return render_template('checkout.html',
                         user=user,
                         cart_items=cart_items,
                         user_addresses=user_addresses,
                         subtotal=subtotal,
                         tax=tax,
                         shipping=shipping,
                         total=total)


@app.route('/order-confirmation/<order_id>')
def order_confirmation(order_id):
    """Order confirmation page"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    order = Order.query.get(order_id)
    
    if not order or order.user_id != session['user_id']:
        return redirect(url_for('index'))
    
    return render_template('order_confirmation.html', order=order)


# ==================== SERVICE BOOKING ====================
@app.route('/services')
def services():
    """Services listing page"""
    services = Service.query.filter_by(is_active=True).all()
    return render_template('services.html', services=services)


@app.route('/service/<slug>/book', methods=['GET', 'POST'])
def book_service(slug):
    """Book a service"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    service = Service.query.filter_by(slug=slug).first_or_404()
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        data = request.form
        
        # Create booking
        booking = ServiceBooking(
            booking_number=f"SRV-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6].upper()}",
            user_id=session['user_id'],
            service_id=service.id,
            device_model=data.get('device_model'),
            problem_description=data.get('problem_description'),
            phone_number=data.get('phone_number'),
            preferred_date=datetime.fromisoformat(data.get('preferred_date')),
            preferred_time=data.get('preferred_time'),
            amount=service.price
        )
        
        db.session.add(booking)
        db.session.commit()
        
        return render_template('service_booking_confirmation.html', booking=booking, service=service)
    
    return render_template('book_service.html', service=service, user=user)


# ==================== USER DASHBOARD ====================
@app.route('/dashboard')
def dashboard():
    """User dashboard"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    orders = Order.query.filter_by(user_id=session['user_id']).order_by(Order.created_at.desc()).all()
    service_bookings = ServiceBooking.query.filter_by(user_id=session['user_id']).order_by(ServiceBooking.created_at.desc()).all()
    
    return render_template('dashboard.html',
                         user=user,
                         orders=orders,
                         service_bookings=service_bookings)


@app.route('/wishlist')
def wishlist():
    """View wishlist"""
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    wishlist_items = Wishlist.query.filter_by(user_id=session['user_id']).all()
    products = [item.product for item in wishlist_items]
    
    return render_template('wishlist.html', products=products)


@app.route('/api/wishlist/add', methods=['POST'])
def add_to_wishlist():
    """Add product to wishlist"""
    if 'user_id' not in session:
        return jsonify({'error': 'Please login first'}), 401
    
    data = request.get_json()
    product_id = data.get('product_id')
    
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    existing = Wishlist.query.filter_by(
        user_id=session['user_id'],
        product_id=product_id
    ).first()
    
    if existing:
        return jsonify({'error': 'Already in wishlist'}), 400
    
    wishlist_item = Wishlist(
        user_id=session['user_id'],
        product_id=product_id
    )
    db.session.add(wishlist_item)
    db.session.commit()
    
    return jsonify({'message': 'Added to wishlist'}), 201


# ==================== ADMIN PANEL ====================
@app.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard"""
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_users = User.query.count()
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
    
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    recent_bookings = ServiceBooking.query.order_by(ServiceBooking.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_products=total_products,
                         total_orders=total_orders,
                         total_users=total_users,
                         total_revenue=total_revenue,
                         recent_orders=recent_orders,
                         recent_bookings=recent_bookings)


@app.route('/admin/products')
def admin_products():
    """Admin product management"""
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    
    query = Product.query
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))
    
    products = query.paginate(page=page, per_page=20, error_out=False)
    categories = Category.query.all()
    brands = Brand.query.all()
    
    return render_template('admin/products.html',
                         products=products,
                         categories=categories,
                         brands=brands)


@app.route('/admin/product/create', methods=['GET', 'POST'])
def admin_create_product():
    """Create new product"""
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    categories = Category.query.all()
    brands = Brand.query.all()
    
    if request.method == 'POST':
        data = request.form
        
        # Check slug uniqueness
        if Product.query.filter_by(slug=data.get('slug')).first():
            return render_template('admin/product_form.html',
                                 categories=categories,
                                 brands=brands,
                                 error='Slug already exists'), 400
        
        product = Product(
            name=data.get('name'),
            slug=data.get('slug'),
            description=data.get('description'),
            category_id=data.get('category_id'),
            brand_id=data.get('brand_id'),
            price=float(data.get('price', 0)),
            discount_percent=float(data.get('discount_percent', 0)),
            stock_quantity=int(data.get('stock_quantity', 0)),
            sku=data.get('sku'),
            is_trending=data.get('is_trending') == 'on',
            is_limited=data.get('is_limited') == 'on'
        )
        
        db.session.add(product)
        db.session.commit()
        
        # Handle image uploads
        if 'images' in request.files:
            for file in request.files.getlist('images'):
                if file and file.filename:
                    filename = secure_filename(f"{product.id}_{uuid.uuid4().hex}.jpg")
                    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    file.save(filepath)
                    
                    product_image = ProductImage(
                        product_id=product.id,
                        image_url=f"/static/uploads/{filename}"
                    )
                    db.session.add(product_image)
        
        db.session.commit()
        return redirect(url_for('admin_products'))
    
    return render_template('admin/product_form.html',
                         categories=categories,
                         brands=brands)


@app.route('/admin/product/<product_id>/edit', methods=['GET', 'POST'])
def admin_edit_product(product_id):
    """Edit product"""
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    product = Product.query.get_or_404(product_id)
    categories = Category.query.all()
    brands = Brand.query.all()
    
    if request.method == 'POST':
        data = request.form
        
        product.name = data.get('name')
        product.slug = data.get('slug')
        product.description = data.get('description')
        product.category_id = data.get('category_id')
        product.brand_id = data.get('brand_id')
        product.price = float(data.get('price', 0))
        product.discount_percent = float(data.get('discount_percent', 0))
        product.stock_quantity = int(data.get('stock_quantity', 0))
        product.sku = data.get('sku')
        product.is_trending = data.get('is_trending') == 'on'
        product.is_limited = data.get('is_limited') == 'on'
        
        db.session.commit()
        return redirect(url_for('admin_products'))
    
    return render_template('admin/product_form.html',
                         product=product,
                         categories=categories,
                         brands=brands)


@app.route('/admin/product/<product_id>/delete', methods=['POST'])
def admin_delete_product(product_id):
    """Delete product"""
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    
    return jsonify({'message': 'Product deleted successfully'}), 200


@app.route('/admin/categories')
def admin_categories():
    """Manage categories"""
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)


@app.route('/admin/category/create', methods=['POST'])
def admin_create_category():
    """Create category"""
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    
    # Check slug uniqueness
    if Category.query.filter_by(slug=data.get('slug')).first():
        return jsonify({'error': 'Slug already exists'}), 400
    
    category = Category(
        name=data.get('name'),
        slug=data.get('slug'),
        description=data.get('description')
    )
    
    db.session.add(category)
    db.session.commit()
    
    return jsonify({'message': 'Category created', 'category_id': category.id}), 201


@app.route('/admin/orders')
def admin_orders():
    """Manage orders"""
    if 'user_id' not in session or not session.get('is_admin'):
        return redirect(url_for('login'))
    
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')
    
    query = Order.query.order_by(Order.created_at.desc())
    
    if status:
        query = query.filter_by(status=status)
    
    orders = query.paginate(page=page, per_page=20, error_out=False)
    
    return render_template('admin/orders.html', orders=orders)


@app.route('/admin/order/<order_id>/update-status', methods=['POST'])
def admin_update_order_status(order_id):
    """Update order status"""
    if 'user_id' not in session or not session.get('is_admin'):
        return jsonify({'error': 'Unauthorized'}), 403
    
    order = Order.query.get_or_404(order_id)
    data = request.get_json()
    
    order.status = data.get('status')
    db.session.commit()
    
    return jsonify({'message': 'Order updated'}), 200


# ==================== CONTACT & FEEDBACK ====================
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page"""
    if request.method == 'POST':
        data = request.form
        
        message = ContactMessage(
            name=data.get('name'),
            email=data.get('email'),
            phone=data.get('phone'),
            subject=data.get('subject'),
            message=data.get('message')
        )
        
        db.session.add(message)
        db.session.commit()
        
        return render_template('contact_confirmation.html')
    
    return render_template('contact.html')


# ==================== ERROR HANDLERS ====================
@app.errorhandler(404)
def page_not_found(error):
    """404 error handler"""
    return render_template('error.html', error='Page not found'), 404


@app.errorhandler(500)
def internal_error(error):
    """500 error handler"""
    db.session.rollback()
    return render_template('error.html', error='Internal server error'), 500


# ==================== DATABASE INITIALIZATION ====================
@app.cli.command()
def init_db():
    """Initialize the database"""
    db.create_all()
    print('Database initialized successfully!')


@app.cli.command()
def seed_db():
    """Seed database with sample data"""
    # Create admin user
    admin = User.query.filter_by(username='admin').first()
    if not admin:
        admin = User(
            username='admin',
            email='admin@devmobile.com',
            is_admin=True,
            first_name='Admin',
            last_name='User'
        )
        admin.set_password('admin123')
        db.session.add(admin)
    
    # Create categories
    categories_data = [
        {'name': 'Smartphones', 'slug': 'smartphones'},
        {'name': 'Chargers', 'slug': 'chargers'},
        {'name': 'Earphones', 'slug': 'earphones'},
        {'name': 'Power Banks', 'slug': 'power-banks'},
        {'name': 'Mobile Covers', 'slug': 'mobile-covers'},
        {'name': 'Screen Protectors', 'slug': 'screen-protectors'},
        {'name': 'Data Cables', 'slug': 'data-cables'},
        {'name': 'Bluetooth Speakers', 'slug': 'bluetooth-speakers'},
    ]
    
    for cat_data in categories_data:
        cat = Category.query.filter_by(slug=cat_data['slug']).first()
        if not cat:
            category = Category(**cat_data)
            db.session.add(category)
    
    # Create brands
    brands_data = [
        {'name': 'Apple', 'slug': 'apple'},
        {'name': 'Samsung', 'slug': 'samsung'},
        {'name': 'Xiaomi', 'slug': 'xiaomi'},
        {'name': 'Realme', 'slug': 'realme'},
        {'name': 'OnePlus', 'slug': 'oneplus'},
        {'name': 'Vivo', 'slug': 'vivo'},
        {'name': 'Oppo', 'slug': 'oppo'},
    ]
    
    for brand_data in brands_data:
        brand = Brand.query.filter_by(slug=brand_data['slug']).first()
        if not brand:
            brand = Brand(**brand_data)
            db.session.add(brand)
    
    # Create services
    services_data = [
        {
            'name': 'Mobile Repair',
            'slug': 'mobile-repair',
            'description': 'Professional mobile phone repair and maintenance',
            'price': 299,
            'duration_minutes': 45,
            'icon': 'fas fa-tools'
        },
        {
            'name': 'Screen Replacement',
            'slug': 'screen-replacement',
            'description': 'Replace broken or damaged mobile screen',
            'price': 499,
            'duration_minutes': 60,
            'icon': 'fas fa-mobile-alt'
        },
        {
            'name': 'Battery Replacement',
            'slug': 'battery-replacement',
            'description': 'Replace battery with genuine part',
            'price': 299,
            'duration_minutes': 30,
            'icon': 'fas fa-battery-full'
        },
        {
            'name': 'Software Update',
            'slug': 'software-update',
            'description': 'Update your device to latest software version',
            'price': 149,
            'duration_minutes': 30,
            'icon': 'fas fa-cogs'
        },
        {
            'name': 'Mobile Unlocking',
            'slug': 'mobile-unlocking',
            'description': 'Unlock your mobile device professionally',
            'price': 399,
            'duration_minutes': 45,
            'icon': 'fas fa-lock-open'
        },
        {
            'name': 'Data Recovery',
            'slug': 'data-recovery',
            'description': 'Recover lost data from your device',
            'price': 599,
            'duration_minutes': 90,
            'icon': 'fas fa-database'
        },
    ]
    
    for service_data in services_data:
        service = Service.query.filter_by(slug=service_data['slug']).first()
        if not service:
            service = Service(**service_data)
            db.session.add(service)
    
    db.session.commit()
    print('Database seeded successfully!')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True, host='0.0.0.0', port=5000)
