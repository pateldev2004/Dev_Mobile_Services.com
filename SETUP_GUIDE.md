# DEV Mobile & Services - Complete Setup & Usage Guide

## 📋 Table of Contents
1. [Project Overview](#overview)
2. [Quick Start](#quick-start)
3. [Default Credentials](#credentials)
4. [File Structure](#file-structure)
5. [Key Features](#features)
6. [Using the Admin Panel](#admin-panel)
7. [Database Schema](#database)
8. [Customization](#customization)
9. [Troubleshooting](#troubleshooting)
10. [Deployment](#deployment)

---

## 📱 Project Overview

**DEV Mobile & Services** is a modern, premium ecommerce and service booking platform built with Flask. It provides:

- ✅ Complete ecommerce functionality (products, cart, checkout)
- ✅ Service booking system (repairs, maintenance, etc.)
- ✅ Admin dashboard for managing products and orders
- ✅ User authentication and profiles
- ✅ Premium, responsive design with Black + Electric Blue theme
- ✅ Mobile-first approach

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Windows/Linux/MacOS

### Step-by-Step Installation

1. **Navigate to Project Directory**
   ```bash
   cd "d:\Dev Mobile & Services"
   ```

2. **Start the Flask Application**
   ```bash
   .\venv\Scripts\python.exe run.py
   ```

3. **Wait for Initialization**
   The server will display:
   ```
   ✓ Database initialized successfully!
   ✓ Default admin user created!
   ✓ Categories created!
   ✓ Brands created!
   ✓ Services created!
   
   🚀 Starting DEV Mobile & Services...
   * Running on http://localhost:5000
   ```

4. **Access the Application**
   - Homepage: http://localhost:5000
   - Admin Dashboard: http://localhost:5000/admin/dashboard
   - Products: http://localhost:5000/products
   - Services: http://localhost:5000/services

---

## 🔐 Default Credentials

### Admin Account
- **Username**: admin
- **Email**: admin@devmobile.com
- **Password**: admin123

⚠️ **IMPORTANT**: Change these credentials immediately after first login in production!

### Test Customer Account
Create your own account through the registration page at `/auth/register`

---

## 📂 File Structure

```
DEV Mobile & Services/
│
├── app.py                    # Main Flask application with all routes
├── models.py                 # Database models (User, Product, Order, etc)
├── config.py                 # Configuration settings
├── run.py                    # Startup script with initialization
├── requirements.txt          # Python dependencies
├── README.md                 # Main documentation
├── SETUP_GUIDE.md           # This file
│
├── templates/               # HTML templates
│   ├── base.html            # Base template with navigation
│   ├── index.html           # Homepage
│   ├── products.html        # Products listing page
│   ├── product_detail.html  # Individual product page
│   ├── cart.html            # Shopping cart
│   ├── checkout.html        # Checkout page
│   ├── services.html        # Services listing
│   ├── contact.html         # Contact form
│   ├── auth/
│   │   ├── login.html       # Login page
│   │   └── register.html    # Registration page
│   ├── admin/
│   │   ├── dashboard.html   # Admin dashboard
│   │   ├── products.html    # Product management
│   │   ├── product_form.html# Create/Edit product
│   │   ├── orders.html      # Order management
│   │   └── categories.html  # Category management
│   └── error.html           # Error page
│
├── static/                  # Static files
│   ├── css/
│   │   └── style.css        # Main stylesheet (14kb)
│   ├── js/
│   │   └── main.js          # Main JavaScript (10kb)
│   └── uploads/             # Product images folder
│
├── venv/                    # Python virtual environment
│   └── Scripts/             # Python executables
│
└── devmobile.db             # SQLite database (auto-created)
```

---

## ✨ Key Features

### 1. **Product Management**
- Create, edit, delete products
- Upload multiple product images
- Set pricing and discounts
- Manage stock levels
- Organize by categories and brands
- Mark products as trending or limited stock

### 2. **Shopping System**
- Advanced product filtering and search
- Shopping cart with quantity management
- Apply discount coupons
- Calculate taxes and shipping
- Multiple payment methods (COD, Card, UPI)

### 3. **Order Management**
- View all orders with status tracking
- Update order status (pending, confirmed, shipped, delivered)
- Track deliveries
- View order history as user

### 4. **Service Booking**
- Browse available services
- Book services with preferred date/time
- Track service booking status
- Service reviews and ratings

### 5. **User System**
- User registration and authentication
- Profile management
- Multiple delivery addresses
- Order history
- Service booking history
- Wishlist functionality

### 6. **Admin Panel**
- Dashboard with key metrics
- Total products, orders, users, revenue
- Recent orders list
- Recent service bookings
- Quick action buttons
- Menu to access all admin features

---

## 👨‍💼 Using the Admin Panel

### Accessing Admin Dashboard

1. Login with admin credentials:
   - URL: http://localhost:5000/auth/login
   - Username: admin
   - Password: admin123

2. You'll be redirected to admin dashboard

### Managing Products

#### Create New Product
1. Click **"Add New Product"** on dashboard or go to **Admin > Products > Create**
2. Fill in the form:
   - **Name**: Product name (e.g., "iPhone 15 Pro")
   - **Slug**: URL-friendly name (auto-generated)
   - **Description**: Detailed product description
   - **Category**: Select from dropdown
   - **Brand**: Select from dropdown
   - **Price**: Original price
   - **Discount %**: Discount percentage
   - **Stock Quantity**: Available units
   - **SKU**: Unique product code
   - **Images**: Upload multiple product images
   - **Mark as Trending**: Checkbox for trending badge
   - **Mark as Limited**: Checkbox for limited stock products

3. Click **Save Product**

#### Edit Product
1. Go to **Admin > Products**
2. Click on product to edit
3. Update information
4. Click **Save**

#### Delete Product
1. Go to **Admin > Products**
2. Click **Delete** button next to product
3. Confirm deletion

### Managing Categories

#### Create Category
1. Go to **Admin > Categories**
2. Click **Add New Category**
3. Enter:
   - **Name**: Category name (e.g., "Smartphones")
   - **Slug**: URL slug (e.g., "smartphones")
   - **Description**: Category description
4. Click **Create**

#### Available Categories
- Smartphones
- Chargers
- Earphones
- Power Banks
- Mobile Covers
- Screen Protectors
- Data Cables
- Bluetooth Speakers

### Managing Orders

#### View Orders
1. Go to **Admin > Orders**
2. View all orders with status
3. Click on order to see details

#### Update Order Status
1. Click on order
2. Select new status:
   - **pending**: Not shipped yet
   - **confirmed**: Confirmed by payment
   - **shipped**: On the way
   - **delivered**: Successfully delivered
   - **cancelled**: Cancelled by user/admin
3. Click **Update**

### Dashboard Metrics

The admin dashboard shows:
- **Total Products**: Count of all products
- **Total Orders**: Count of all orders
- **Total Users**: Count of registered users
- **Total Revenue**: Sum of all order totals

---

## 🗄️ Database Schema

### Key Tables

#### Users
- username, email, password_hash
- first_name, last_name, phone
- is_admin (boolean)
- created_at, updated_at

#### Products
- name, slug, description
- category_id, brand_id
- price, discount_percent
- stock_quantity, sku
- rating, review_count
- is_trending, is_limited
- created_at, updated_at

#### Orders
- order_number (unique)
- user_id
- status (pending, confirmed, shipped, delivered, cancelled)
- payment_method, payment_status
- subtotal, tax, shipping, discount, total_amount
- delivery_address, tracking_number
- created_at, updated_at

#### Services
- name, slug, description
- price, duration_minutes
- icon, rating, review_count
- is_active

#### ServiceBooking
- booking_number (unique)
- user_id, service_id
- device_model, problem_description
- preferred_date, preferred_time
- status, amount
- created_at, updated_at

#### Other Tables
- ProductImage (product images)
- Category (product categories)
- Brand (product brands)
- CartItem (shopping cart)
- OrderItem (items in orders)
- Review (product reviews)
- Wishlist (user favorites)
- Address (delivery addresses)
- Coupon (discount codes)
- ContactMessage (contact form submissions)

---

## 🎨 Customization

### Change Site Colors
Edit `/static/css/style.css`:

```css
:root {
    --primary-dark: #0a0e27;        /* Main dark color */
    --electric-blue: #00d4ff;       /* Accent color */
    --accent-blue: #0066ff;         /* Primary button color */
}
```

### Customize Brands
Edit the brand list in `models.py` seed function

### Change Business Details
Update in `base.html` footer:
- Phone number
- Email
- Address
- Social media links
- Business hours

### Modify Payment Methods
Edit checkout form in `templates/checkout.html`

---

## 🔧 Troubleshooting

### Application Won't Start

**Error**: "ModuleNotFoundError: No module named 'flask'"

**Solution**:
```bash
.\venv\Scripts\pip.exe install -r requirements.txt
```

### Database Issues

**Error**: "Database locked"

**Solution**:
1. Delete `devmobile.db` file
2. Restart the application
3. Database will be recreated

### Static Files Not Loading

**Issue**: CSS/JS not loading (404 errors)

**Solution**:
1. Check if `/static` folder exists
2. Restart the application
3. Clear browser cache (Ctrl+Shift+Delete)

### Login Not Working

**Error**: "Invalid credentials"

**Solution**:
1. Ensure you're using correct credentials
2. Default: username=`admin`, password=`admin123`
3. Check if user exists in admin panel

---

## 🚀 Deployment

### Prepare for Production

1. **Change Secret Key**
   ```python
   # In config.py
   SECRET_KEY = 'your-secure-random-key'
   ```

2. **Disable Debug Mode**
   ```python
   # In config.py
   DEBUG = False
   ```

3. **Use PostgreSQL** (instead of SQLite)
   ```python
   SQLALCHEMY_DATABASE_URI = 'postgresql://user:password@localhost/devmobile'
   ```

4. **Set Environment Variables**
   ```bash
   FLASK_ENV=production
   SECRET_KEY=your-secret-key
   ```

### Deploy with Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Deploy with Docker

Create `Dockerfile`:
```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

Build and run:
```bash
docker build -t devmobile .
docker run -p 5000:5000 devmobile
```

---

## 📈 Next Steps

After setup, consider:
1. Add SSL certificate for HTTPS
2. Set up email notifications
3. Integrate payment gateway (Stripe/Razorpay)
4. Add SMS notifications
5. Create blog/tips section
6. Add customer reviews system
7. Implement analytics
8. Set up monitoring and logging

---

## 📞 Support

For issues or questions:
- Email: support@devmobile.com
- Phone: +91 98765 43210
- GitHub: [Create an issue]

---

**Happy selling! 🎉**

Made with ❤️ for DEV Mobile & Services
