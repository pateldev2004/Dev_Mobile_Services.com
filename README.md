# DEV Mobile & Services - Premium eCommerce Platform

A comprehensive, modern ecommerce and service booking platform built with Flask, featuring product management, shopping cart, service booking, and a powerful admin dashboard.

## Features

### 🛍️ Shopping System
- Browse products by categories and brands
- Advanced filtering (price, brand, category)
- Product search functionality
- Shopping cart management
- Multiple payment methods (COD, UPI, Card)
- Order tracking and history
- Wishlist functionality
- Coupon/discount codes

### 🔧 Service Booking
- Book professional repair services
- Service types: Mobile Repair, Screen Replacement, Battery Replacement, Software Update, Unlocking, Data Recovery
- Service scheduling and tracking
- Same-day service options
- Service history

### 👨‍💼 Admin Dashboard
- Manage products (create, edit, delete)
- Product image uploads
- Inventory management
- Category and brand management
- Order management and tracking
- Service booking management
- Customer feedback monitoring

### 👤 User Features
- User registration and authentication
- User profile and dashboard
- Order history
- Service booking history
- Multiple delivery addresses
- Wishlist management
- Account settings

### 🎨 Premium Design
- Modern Black + Electric Blue + White theme
- Mobile-first responsive design
- Smooth animations and transitions
- Professional typography
- Dark mode support
- Fast loading times

## Tech Stack

- **Backend**: Flask 3.1.3 (Python)
- **Database**: SQLite (SQLAlchemy ORM)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Authentication**: Werkzeug (password hashing)
- **API**: RESTful Flask endpoints

## Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Setup Steps

1. **Clone or Navigate to Project Directory**
   ```bash
   cd "d:\Dev Mobile & Services"
   ```

2. **Create Virtual Environment** (if not already created)
   ```bash
   python -m venv venv
   ```

3. **Activate Virtual Environment**
   - Windows (PowerShell):
     ```bash
     .\venv\Scripts\Activate.ps1
     ```
   - Windows (Command Prompt):
     ```bash
     venv\Scripts\activate.bat
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Initialize Database**
   ```bash
   python app.py
   ```
   
   Then in Python shell:
   ```python
   from app import app, db
   with app.app_context():
       db.create_all()
   ```

6. **Seed Sample Data** (Optional)
   ```python
   from app import app
   with app.app_context():
       from app import seed_db
       # Run seed_db command
   ```

## Running the Application

```bash
python app.py
```

The application will start at `http://localhost:5000`

## Default Admin Account

- **Username**: admin
- **Email**: admin@devmobile.com
- **Password**: admin123

⚠️ **Important**: Change this password immediately in production!

## Project Structure

```
DEV Mobile & Services/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── models.py              # Database models
├── requirements.txt       # Python dependencies
├── templates/
│   ├── base.html         # Base template
│   ├── index.html        # Homepage
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   ├── admin/            # Admin dashboard templates
│   ├── product_detail.html
│   ├── products.html
│   └── ...
├── static/
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   ├── js/
│   │   └── main.js       # Main JavaScript
│   └── uploads/          # Product images
└── venv/                 # Virtual environment
```

## Core Models

### User
- Username, Email, Password (hashed)
- Admin flag
- Personal information (name, phone)

### Product
- Name, Description, Price
- Stock management
- Discount percentage
- Trending and limited stock flags
- Category and Brand relationships
- Images and Reviews

### Order
- Order number (unique)
- User and order items
- Payment method and status
- Pricing breakdown (subtotal, tax, shipping, discount)
- Delivery tracking

### Service
- Service name and description
- Price and duration
- Rating and reviews

### ServiceBooking
- Booking number
- Service and user relationship
- Device information
- Preferred date and time
- Status tracking

### Category & Brand
- Organized product structure
- Active flag for visibility

### Wishlist
- User product favorites
- Easy product saving

### Coupon
- Discount code management
- Percentage and fixed amount discounts
- Valid date ranges
- Usage limits

## Key Features Breakdown

### Shopping Cart
- Add/remove products
- Update quantities
- Real-time totals calculation
- Applied discounts display

### Checkout Flow
1. View cart
2. Enter delivery address
3. Review order
4. Select payment method
5. Order confirmation with SMS/Email

### Admin Panel
- Dashboard with key metrics
- Product CRUD operations
- Category management
- Order tracking and status updates
- Service booking management
- Customer contact management

### Product Management
- Create products with multiple images
- Set pricing and discounts
- Manage stock levels
- Mark as trending or limited
- Organize by category and brand

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - User login
- `GET /auth/logout` - User logout

### Products
- `GET /products` - List products (with filters)
- `GET /product/<slug>` - Product details

### Shopping Cart
- `POST /api/cart/add` - Add to cart
- `POST /api/cart/remove` - Remove from cart
- `GET /cart` - View cart

### Wishlist
- `POST /api/wishlist/add` - Add to wishlist

### Orders
- `GET /checkout` - Checkout page
- `POST /checkout` - Create order
- `GET /order-confirmation/<order_id>` - Order confirmation

### Services
- `GET /services` - List services
- `POST /service/<slug>/book` - Book service

### Admin
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/products` - Manage products
- `POST /admin/product/create` - Create product
- `POST /admin/product/<id>/edit` - Edit product
- `POST /admin/product/<id>/delete` - Delete product
- `GET /admin/orders` - Manage orders
- `POST /admin/order/<id>/update-status` - Update order status

## Configuration

Edit `config.py` to customize:
- Database URI
- Secret key
- Session settings
- File upload settings
- Email configuration
- Payment gateway credentials

## Security Features

- Password hashing with Werkzeug
- Session management
- CSRF protection ready
- SQL Injection prevention (SQLAlchemy ORM)
- Secure password reset flow
- Admin authentication

## Performance Optimizations

- CSS Grid for efficient layouts
- Image lazy loading
- Efficient database queries
- Caching ready
- Minified CSS and JS
- Fast JSON APIs

## Deployment

For production deployment:

1. Change `SECRET_KEY` in config.py
2. Set `DEBUG = False`
3. Use a production WSGI server (Gunicorn, uWSGI)
4. Set up proper database (PostgreSQL recommended)
5. Enable HTTPS
6. Configure email service for notifications
7. Set up payment gateway (Stripe)

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Future Enhancements

- [ ] SMS and Email notifications
- [ ] Payment gateway integration (Stripe, Razorpay)
- [ ] Advanced analytics dashboard
- [ ] Customer review system
- [ ] Blog and tips section
- [ ] Video reels integration
- [ ] Push notifications
- [ ] Referral program
- [ ] Live chat support
- [ ] Multi-language support

## Support

For issues, bugs, or feature requests, please create an issue or contact support.

## License

This project is proprietary software for DEV Mobile & Services.

## Contact

- **Website**: www.devmobile.com
- **Email**: info@devmobile.com
- **Phone**: +91 98765 43210

---

Made with ❤️ for DEV Mobile & Services
