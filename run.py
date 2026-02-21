#!/usr/bin/env python
"""
DEV Mobile & Services - Application Startup Script
"""

from app import app, db

if __name__ == '__main__':
    # Create tables
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✓ Database initialized successfully!")
        
        # Check if admin user exists, if not create it
        from models import User, Category, Brand, Service
        
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("\nCreating default admin user...")
            admin = User(
                username='admin',
                email='admin@devmobile.com',
                is_admin=True,
                first_name='Admin',
                last_name='User'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✓ Default admin user created!")
            print("  Username: admin")
            print("  Email: admin@devmobile.com")
            print("  Password: admin123")
        
        # Create sample categories if none exist
        if Category.query.count() == 0:
            print("\nCreating sample categories...")
            categories = [
                Category(name='Smartphones', slug='smartphones', is_active=True),
                Category(name='Chargers', slug='chargers', is_active=True),
                Category(name='Earphones', slug='earphones', is_active=True),
                Category(name='Power Banks', slug='power-banks', is_active=True),
                Category(name='Mobile Covers', slug='mobile-covers', is_active=True),
                Category(name='Screen Protectors', slug='screen-protectors', is_active=True),
                Category(name='Data Cables', slug='data-cables', is_active=True),
                Category(name='Bluetooth Speakers', slug='bluetooth-speakers', is_active=True),
            ]
            db.session.add_all(categories)
            db.session.commit()
            print("✓ Categories created!")
        
        # Create sample brands if none exist
        if Brand.query.count() == 0:
            print("\nCreating sample brands...")
            brands = [
                Brand(name='Apple', slug='apple', is_active=True),
                Brand(name='Samsung', slug='samsung', is_active=True),
                Brand(name='Xiaomi', slug='xiaomi', is_active=True),
                Brand(name='Realme', slug='realme', is_active=True),
                Brand(name='OnePlus', slug='oneplus', is_active=True),
                Brand(name='Vivo', slug='vivo', is_active=True),
                Brand(name='Oppo', slug='oppo', is_active=True),
            ]
            db.session.add_all(brands)
            db.session.commit()
            print("✓ Brands created!")
        
        # Create sample services if none exist
        if Service.query.count() == 0:
            print("\nCreating sample services...")
            services = [
                Service(
                    name='Mobile Repair',
                    slug='mobile-repair',
                    description='Professional mobile phone repair and maintenance',
                    price=299,
                    duration_minutes=45,
                    icon='fas fa-tools',
                    is_active=True
                ),
                Service(
                    name='Screen Replacement',
                    slug='screen-replacement',
                    description='Replace broken or damaged mobile screen',
                    price=499,
                    duration_minutes=60,
                    icon='fas fa-mobile-alt',
                    is_active=True
                ),
                Service(
                    name='Battery Replacement',
                    slug='battery-replacement',
                    description='Replace battery with genuine part',
                    price=299,
                    duration_minutes=30,
                    icon='fas fa-battery-full',
                    is_active=True
                ),
                Service(
                    name='Software Update',
                    slug='software-update',
                    description='Update your device to latest software version',
                    price=149,
                    duration_minutes=30,
                    icon='fas fa-cogs',
                    is_active=True
                ),
                Service(
                    name='Mobile Unlocking',
                    slug='mobile-unlocking',
                    description='Unlock your mobile device professionally',
                    price=399,
                    duration_minutes=45,
                    icon='fas fa-lock-open',
                    is_active=True
                ),
                Service(
                    name='Data Recovery',
                    slug='data-recovery',
                    description='Recover lost data from your device',
                    price=599,
                    duration_minutes=90,
                    icon='fas fa-database',
                    is_active=True
                ),
            ]
            db.session.add_all(services)
            db.session.commit()
            print("✓ Services created!")
    
    print("\n" + "="*50)
    print("🚀 Starting DEV Mobile & Services...")
    print("="*50)
    print("\n✓ Application ready!")
    print("\n📍 Access the application at:")
    print("   http://localhost:5000")
    print("\n📍 Admin Dashboard:")
    print("   http://localhost:5000/admin/dashboard")
    print("\n📍 Default Admin Credentials:")
    print("   Username: admin")
    print("   Password: admin123")
    print("\n⚠️  Change admin password immediately in production!")
    print("\n" + "="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
