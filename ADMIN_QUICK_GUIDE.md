# 🎯 Admin Quick Reference Guide

## Quick Navigation

### Admin Dashboard Access
```
URL: http://localhost:5000/admin/dashboard
Login: admin / admin123
```

---

## 🛍️ Product Management

### Add Product (5 minutes)
1. Admin Dashboard → Click "Add New Product"
2. Fill form:
   - Name: (e.g., "Samsung Galaxy S24")
   - Category: (dropdown)
   - Brand: (dropdown)
   - Price: ₹
   - Discount %: (e.g., 10)
   - Stock: (quantity)
3. Upload Images
4. Save

### Edit Product (3 minutes)
1. Admin → Products
2. Click product name
3. Edit fields
4. Save

### Delete Product (1 minute)
1. Admin → Products
2. Click Delete button
3. Confirm

### Key Fields
| Field | Example | Notes |
|-------|---------|-------|
| Name | iPhone 15 Pro | Product name |
| Slug | iphone-15-pro | Auto-generated |
| Category | Smartphones | Select category |
| Brand | Apple | Select brand |
| Price | 99999 | Original price (₹) |
| Discount | 10 | Percentage (%) |
| Stock | 50 | Available units |
| SKU | IP15PRO001 | Unique code |
| Images | Upload 3-5 | Multiple images |
| Trending | Checkbox | For trending badge |
| Limited | Checkbox | For limited stock badge |

---

##  📦 Category Management

### Add Category
1. Admin → Categories → Add New
2. Name: (e.g., "Smartphones")
3. Slug: (e.g., "smartphones")
4. Save

### Pre-loaded Categories
- Smartphones
- Chargers
- Earphones
- Power Banks
- Mobile Covers
- Screen Protectors
- Data Cables
- Bluetooth Speakers

---

## 🏷️ Brand Management

### Add Brand
1. Admin → Brands → Add New
2. Name: (e.g., "Apple")
3. Logo URL: (optional)
4. Save

### Pre-loaded Brands
- Apple
- Samsung
- Xiaomi
- Realme
- OnePlus
- Vivo
- Oppo

---

## 📋 Order Management

### View Orders
1. Admin → Orders
2. Click order number to see details

### Update Order Status
1. Admin → Orders
2. Click on order
3. Change Status:
   - **pending** → Not begun
   - **confirmed** → Payment received
   - **shipped** → On the way
   - **delivered** → Successfully delivered
   - **cancelled** → Cancelled

---

## 💰 Pricing Guide

### Discounts
- Set percentage discount
- Automatically calculates final price
- Shows savings amount to customers
- Example: ₹1000 with 10% discount = ₹900

### Taxes
- Automatically 18% GST
- Added at checkout
- Shown in order summary

### Shipping
- ₹50 base shipping
- Free for orders > ₹499
- Calculated at checkout

---

## 📊 Dashboard Metrics

### Key Numbers to Monitor
- **Total Products**: Count of all products
- **Total Orders**: Count of all transactions
- **Total Users**: Registered customers
- **Total Revenue**: Sum of all order values

### Recent Orders
- Shows last 10 orders
- Status at a glance
- Quick action links

---

## 🔧 Service Management

### Available Services (Pre-configured)
1. **Mobile Repair** - ₹299, 45 min
2. **Screen Replacement** - ₹499, 60 min
3. **Battery Replacement** - ₹299, 30 min
4. **Software Update** - ₹149, 30 min
5. **Mobile Unlocking** - ₹399, 45 min
6. **Data Recovery** - ₹599, 90 min

### Edit Service Price
1. Admin → Services (Coming soon)
2. Edit service
3. Update price
4. Save

---

## 💳 Payment Methods

### Available Payment Options
- **Card**: Credit/Debit card (ready to integrate)
- **UPI**: Digital payments (ready to integrate)
- **COD**: Cash on Delivery (enabled)

### Next Steps
- Integrate Stripe or Razorpay
- Add payment processing
- Implement webhooks

---

## 👥 User Management

### View Users
- Admin → Dashboard
- Total users count displayed
- User list coming soon

### User Data Available
- Username & Email
- Registration date
- Phone number
- Addresses
- Order history
- Service bookings

---

## 📧 Contact Messages

### View Messages
- Admin → Contact (coming soon)
- View all contact form submissions
- Mark as read/replied

### Message Fields
- Name
- Email
- Phone
- Subject
- Message
- Received date

---

## 📈 Daily Operations

### Morning Checklist
- [ ] Check new orders
- [ ] Update order statuses
- [ ] Review service bookings
- [ ] Check contact messages
- [ ] Monitor stock levels

### Weekly Tasks
- [ ] Update discounts
- [ ] Add new products
- [ ] Review customer feedback
- [ ] Check revenue

### Monthly Tasks
- [ ] Analyze sales trends
- [ ] Update inventory
- [ ] Plan promotions
- [ ] Backup database

---

## 🎯 Best Practices

### Product Images
- Use high-quality images (minimum 500x500px)
- Upload 3-5 images per product
- Include different angles
- Show product in use (optional)

### Pricing Strategy
- Monitor competitor prices
- Offer seasonal discounts (10-30%)
- Use limited stock to create urgency
- Mark trending products

### Inventory Management
- Keep stock updated
- Alert when stock < 5 units
- Remove out-of-stock items
- Regular physical count

### Customer Service
- Respond to contact messages quickly
- Update order status promptly
- Honor service warranties
- Collect customer feedback

---

## ⚙️ Technical Tasks

### Database Backup
```bash
# Backup database before major changes
copy devmobile.db devmobile_backup.db
```

### Restart Application
```bash
# Stop: Press Ctrl+C in terminal
# Start: .\venv\Scripts\python.exe run.py
```

### Clear Cache
- Browser: Ctrl+Shift+Delete
- App: Delete `devmobile.db` and restart

---

## 🔐 Security Tasks

### Change Admin Password
1. In database (admin user table)
2. Use secure random password
3. Update in secure location

### Backup Database
- Daily backups recommended
- Keep version history
- Store securely

### Access Control
- Only share admin credentials if necessary
- Change password every 3 months
- Monitor admin activity

---

## 📱 Mobile App Considerations

### Mobile-Friendly Features
✓ Responsive design (mobile first)
✓ Touch-friendly buttons
✓ Fast loading
✓ Mobile checkout
✓ App-like experience

### Mobile Testing
- Test on iPhone 12/13/14
- Test on Android (Samsung, Xiaomi)
- Test on tablets
- Check landscape mode

---

## 🚀 Promotion Tips

### Flash Deals
```
Create limited stock items
Set 20-30% discount
Add countdown timer
Highlight with badge
```

### Seasonal Promotions
```
Diwali - 30-40% discount
New Year - Free shipping
Summer Sale - Mix of discounts
Festival seasons - Extra promotions
```

### Bundle Offers
```
Combine products
Create package deals
Offer discount on bundle
Display prominently
```

---

## 📊 Reports to Monitor

### Sales Reports (to add)
- Daily/Weekly/Monthly sales
- Top selling products
- Revenue trends
- Customer acquisition

### Inventory Reports (to add)
- Stock levels
- Fast-moving items
- Slow inventory
- Stock alerts

### Customer Reports (to add)
- New customers
- Repeat purchases
- Customer lifetime value
- Churn rate

---

## Common Issues & Solutions

### Product Not Showing
**Problem**: Created product not visible
**Solution**: 
- Check `is_active` checkbox
- Verify category exists
- Refresh browser cache

### Order Status Not Updating
**Problem**: Status change not saving
**Solution**:
- Refresh page
- Restart application
- Check database connection

### Image Upload Failed
**Problem**: Images not uploading
**Solution**:
- Check file size (max 16MB)
- Verify format (JPG, PNG)
- Check folder permissions

---

## 📞 Support Commands

### Check App Status
```bash
# In another terminal, test API
curl http://localhost:5000/
# Should show homepage
```

### View Database
```bash
# Install DB browser (optional)
# Open devmobile.db with SQLite viewer
```

---

## 🎓 Training for Team

### New Admin Training
1. Show homepage & products
2. Demo product creation
3. Show order management
4. Explain dashboard metrics
5. Walk through contact messages

### Estimated Time
- Basic training: 1 hour
- Advanced features: 2-3 hours
- Full mastery: 1 week

---

## 📋 Quick Checklist

### Before Launch
- [ ] Change admin password
- [ ] Customize business details
- [ ] Add real product images
- [ ] Set up email (optional)
- [ ] Configure payment gateway
- [ ] Test all features
- [ ] Check mobile responsiveness

### Weekly Maintenance
- [ ] Backup database
- [ ] Review orders
- [ ] Update inventory
- [ ] Check error logs
- [ ] Monitor performance

### Monthly Review
- [ ] Analyze sales
- [ ] Plan promotions
- [ ] Update content
- [ ] Review security
- [ ] Optimize performance

---

## 💡 Pro Tips

1. **Bulk Upload**: Create product template, upload multiple at once
2. **Smart Pricing**: Use psychological pricing ($99 instead of $100)
3. **Stock Management**: Keep 10-20% extra for seasonal demand
4. **Image Optimization**: Compress images for faster loading
5. **SEO**: Use descriptive product names and descriptions
6. **Reviews**: Ask customers for feedback on orders
7. **Email**: Send order updates and promotions
8. **Analytics**: Track which products sell best

---

## 🎯 Success Metrics

### Track These:
- Total Orders Per Day
- Average Order Value
- Customer Satisfaction
- Product Performance
- Service Utilization
- Revenue Growth
- Customer Retention

---

**Ready to manage your store?**

Start with: http://localhost:5000/admin/dashboard

Login: admin / admin123 (Change password immediately!)

---

*This guide is your daily reference for admin tasks.*
*Keep this document handy!*
