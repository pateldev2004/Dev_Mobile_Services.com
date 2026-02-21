"""
Database models for DEV Mobile & Services
"""

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid

db = SQLAlchemy()


class User(db.Model):
    """User model for authentication and customer profiles"""
    __tablename__ = 'users'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(15))
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    addresses = db.relationship('Address', backref='user', lazy=True, cascade='all, delete-orphan')
    cart_items = db.relationship('CartItem', backref='user', lazy=True, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='user', lazy=True, cascade='all, delete-orphan')
    service_bookings = db.relationship('ServiceBooking', backref='user', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='user', lazy=True, cascade='all, delete-orphan')
    wishlist_items = db.relationship('Wishlist', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Address(db.Model):
    """Delivery addresses for users"""
    __tablename__ = 'addresses'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    address_type = db.Column(db.String(20), default='home')  # home, work, other
    street = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    postal_code = db.Column(db.String(20), nullable=False)
    country = db.Column(db.String(100), default='India')
    phone = db.Column(db.String(15), nullable=False)
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Address {self.city}>'


class Category(db.Model):
    """Product categories"""
    __tablename__ = 'categories'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='category', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Category {self.name}>'


class Brand(db.Model):
    """Product brands"""
    __tablename__ = 'brands'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), unique=True, nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    logo_url = db.Column(db.String(500))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='brand', lazy=True)
    
    def __repr__(self):
        return f'<Brand {self.name}>'


class Product(db.Model):
    """Product model"""
    __tablename__ = 'products'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(200), nullable=False, index=True)
    slug = db.Column(db.String(200), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    category_id = db.Column(db.String(36), db.ForeignKey('categories.id'), nullable=False)
    brand_id = db.Column(db.String(36), db.ForeignKey('brands.id'))
    price = db.Column(db.Float, nullable=False)
    discount_percent = db.Column(db.Float, default=0)
    stock_quantity = db.Column(db.Integer, default=0)
    sku = db.Column(db.String(100), unique=True)
    rating = db.Column(db.Float, default=0)
    review_count = db.Column(db.Integer, default=0)
    is_trending = db.Column(db.Boolean, default=False)
    is_limited = db.Column(db.Boolean, default=False)  # Limited stock items
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    images = db.relationship('ProductImage', backref='product', lazy=True, cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='product', lazy=True, cascade='all, delete-orphan')
    cart_items = db.relationship('CartItem', backref='product', lazy=True, cascade='all, delete-orphan')
    order_items = db.relationship('OrderItem', backref='product', lazy=True, cascade='all, delete-orphan')
    wishlist_items = db.relationship('Wishlist', backref='product', lazy=True, cascade='all, delete-orphan')
    
    @property
    def discounted_price(self):
        """Calculate discounted price"""
        if self.discount_percent > 0:
            return round(self.price * (1 - self.discount_percent / 100), 2)
        return self.price
    
    @property
    def savings(self):
        """Calculate savings amount"""
        return round(self.price - self.discounted_price, 2)
    
    def __repr__(self):
        return f'<Product {self.name}>'


class ProductImage(db.Model):
    """Product images"""
    __tablename__ = 'product_images'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    alt_text = db.Column(db.String(200))
    is_primary = db.Column(db.Boolean, default=False)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ProductImage {self.product_id}>'


class Wishlist(db.Model):
    """User wishlist"""
    __tablename__ = 'wishlist'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'product_id', name='unique_wishlist'),)
    
    def __repr__(self):
        return f'<Wishlist {self.user_id}-{self.product_id}>'


class CartItem(db.Model):
    """Shopping cart items"""
    __tablename__ = 'cart_items'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'product_id', name='unique_cart_item'),)
    
    @property
    def total_price(self):
        """Calculate total price for this item"""
        return self.product.discounted_price * self.quantity
    
    def __repr__(self):
        return f'<CartItem {self.user_id}-{self.product_id}>'


class Order(db.Model):
    """Customer orders"""
    __tablename__ = 'orders'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, confirmed, shipped, delivered, cancelled
    payment_method = db.Column(db.String(50))  # card, upi, cod
    payment_status = db.Column(db.String(50), default='pending')  # pending, completed, failed
    
    # Pricing
    subtotal = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, default=0)
    shipping = db.Column(db.Float, default=0)
    discount = db.Column(db.Float, default=0)
    total_amount = db.Column(db.Float, nullable=False)
    
    # Delivery details
    delivery_address = db.Column(db.Text)  # Store address as JSON or text
    estimated_delivery = db.Column(db.DateTime)
    delivered_at = db.Column(db.DateTime)
    
    # Tracking
    tracking_number = db.Column(db.String(100))
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order_items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.order_number}>'


class OrderItem(db.Model):
    """Individual items in an order"""
    __tablename__ = 'order_items'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    order_id = db.Column(db.String(36), db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)  # Price at time of order
    discount_amount = db.Column(db.Float, default=0)
    
    def __repr__(self):
        return f'<OrderItem {self.order_id}-{self.product_id}>'


class Service(db.Model):
    """Service offerings"""
    __tablename__ = 'services'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    price = db.Column(db.Float, nullable=False)
    duration_minutes = db.Column(db.Integer, default=30)
    icon = db.Column(db.String(50))  # Font Awesome class
    rating = db.Column(db.Float, default=0)
    review_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    service_bookings = db.relationship('ServiceBooking', backref='service', lazy=True, cascade='all, delete-orphan')
    service_reviews = db.relationship('ServiceReview', backref='service', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Service {self.name}>'


class ServiceBooking(db.Model):
    """Service booking/reservation"""
    __tablename__ = 'service_bookings'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    booking_number = db.Column(db.String(20), unique=True, nullable=False, index=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    service_id = db.Column(db.String(36), db.ForeignKey('services.id'), nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, confirmed, completed, cancelled
    
    # Service details
    device_model = db.Column(db.String(100))
    problem_description = db.Column(db.Text)
    phone_number = db.Column(db.String(15), nullable=False)
    
    # Booking details
    preferred_date = db.Column(db.DateTime, nullable=False)
    preferred_time = db.Column(db.String(20))  # e.g., "10:00-11:00"
    amount = db.Column(db.Float, nullable=False)
    
    # Completion
    completed_at = db.Column(db.DateTime)
    notes = db.Column(db.Text)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ServiceBooking {self.booking_number}>'


class Review(db.Model):
    """Product reviews"""
    __tablename__ = 'reviews'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    product_id = db.Column(db.String(36), db.ForeignKey('products.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    title = db.Column(db.String(200))
    comment = db.Column(db.Text)
    helpful_count = db.Column(db.Integer, default=0)
    is_verified = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Review {self.product_id}-{self.user_id}>'


class ServiceReview(db.Model):
    """Service reviews"""
    __tablename__ = 'service_reviews'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    service_id = db.Column(db.String(36), db.ForeignKey('services.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ServiceReview {self.service_id}-{self.user_id}>'


class Coupon(db.Model):
    """Discount coupons"""
    __tablename__ = 'coupons'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    discount_type = db.Column(db.String(20), default='percent')  # percent or fixed
    discount_value = db.Column(db.Float, nullable=False)
    min_purchase = db.Column(db.Float, default=0)
    max_uses = db.Column(db.Integer)
    used_count = db.Column(db.Integer, default=0)
    valid_from = db.Column(db.DateTime, nullable=False)
    valid_until = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def is_valid(self):
        """Check if coupon is valid"""
        now = datetime.utcnow()
        return (self.is_active and 
                self.valid_from <= now <= self.valid_until and
                (self.max_uses is None or self.used_count < self.max_uses))
    
    def __repr__(self):
        return f'<Coupon {self.code}>'


class ContactMessage(db.Model):
    """Contact form messages"""
    __tablename__ = 'contact_messages'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(15))
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(50), default='new')  # new, read, replied
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ContactMessage {self.email}>'
