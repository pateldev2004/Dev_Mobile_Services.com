/* DEV Mobile & Services - Main JavaScript */

// Initialize tooltips
document.addEventListener('DOMContentLoaded', function() {
    // Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Update cart count
    updateCartCount();
    updateWishlistCount();
});

// Add to cart function
function addToCart(productId, quantity = 1) {
    if (!productId) {
        showAlert('Product not found', 'error');
        return;
    }
    
    fetch('/api/cart/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: quantity
        })
    })
    .then(response => response.json())
    .then(data => {
        if (response.status === 401) {
            window.location.href = '/auth/login';
            return;
        }
        showAlert(data.message, response.ok ? 'success' : 'error');
        if (response.ok) {
            updateCartCount();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Failed to add to cart', 'error');
    });
}

// Remove from cart function
function removeFromCart(productId) {
    if (!confirm('Remove this item from cart?')) return;
    
    fetch('/api/cart/remove', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            product_id: productId
        })
    })
    .then(response => response.json())
    .then(data => {
        showAlert(data.message, response.ok ? 'success' : 'error');
        if (response.ok) {
            location.reload();
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Failed to remove item', 'error');
    });
}

// Add to wishlist function
function addToWishlist(productId) {
    fetch('/api/wishlist/add', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            product_id: productId
        })
    })
    .then(response => response.json())
    .then(data => {
        if (response.status === 401) {
            window.location.href = '/auth/login';
            return;
        }
        showAlert(data.message, response.ok ? 'success' : 'error');
        if (response.ok) {
            updateWishlistCount();
            // Update button state
            const btn = document.querySelector(`[data-product="${productId}"] .btn-wishlist`);
            if (btn) {
                btn.classList.add('active');
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        showAlert('Failed to add to wishlist', 'error');
    });
}

// Update cart count
function updateCartCount() {
    const cartCountElement = document.getElementById('cart-count');
    if (!cartCountElement) return;
    
    fetch('/api/cart/count')
    .then(response => response.json())
    .then(data => {
        cartCountElement.textContent = data.count;
    })
    .catch(error => console.error('Error:', error));
}

// Update wishlist count
function updateWishlistCount() {
    const wishlistCountElement = document.getElementById('wishlist-count');
    if (!wishlistCountElement) return;
    
    fetch('/api/wishlist/count')
    .then(response => response.json())
    .then(data => {
        wishlistCountElement.textContent = data.count;
    })
    .catch(error => console.error('Error:', error));
}

// Show alert function
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${getAlertClass(type)} alert-dismissible fade show`;
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container-fluid') || document.querySelector('.container');
    if (container) {
        container.insertAdjacentElement('afterbegin', alertDiv);
    }
    
    setTimeout(() => {
        alertDiv.remove();
    }, 5000);
}

function getAlertClass(type) {
    const classes = {
        'success': 'success',
        'error': 'danger',
        'warning': 'warning',
        'info': 'info'
    };
    return classes[type] || 'info';
}

// Format price
function formatPrice(price) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR',
        minimumFractionDigits: 0
    }).format(price);
}

// Update cart quantity
function updateQuantity(productId, quantity) {
    quantity = parseInt(quantity);
    if (quantity <= 0) {
        removeFromCart(productId);
        return;
    }
    
    // Store for backend update
    const input = document.querySelector(`input[data-product="${productId}"]`);
    if (input) {
        input.value = quantity;
    }
    
    // Recalculate totals
    recalculateCart();
}

// Recalculate cart totals
function recalculateCart() {
    const items = document.querySelectorAll('.cart-item');
    let subtotal = 0;
    
    items.forEach(item => {
        const price = parseFloat(item.dataset.price);
        const quantity = parseInt(item.querySelector('input[type="number"]').value);
        subtotal += price * quantity;
    });
    
    const tax = subtotal * 0.18;
    const shipping = subtotal > 0 ? 50 : 0;
    const total = subtotal + tax + shipping;
    
    // Update display
    document.getElementById('subtotal') && (document.getElementById('subtotal').textContent = formatPrice(subtotal));
    document.getElementById('tax') && (document.getElementById('tax').textContent = formatPrice(tax));
    document.getElementById('shipping') && (document.getElementById('shipping').textContent = formatPrice(shipping));
    document.getElementById('total') && (document.getElementById('total').textContent = formatPrice(total));
}

// Filter products
function filterProducts() {
    const category = document.getElementById('category')?.value;
    const brand = document.getElementById('brand')?.value;
    const minPrice = document.getElementById('minPrice')?.value;
    const maxPrice = document.getElementById('maxPrice')?.value;
    const search = document.getElementById('search')?.value;
    const sort = document.getElementById('sort')?.value;
    
    let url = '/products?page=1';
    if (category) url += `&category=${category}`;
    if (brand) url += `&brand=${brand}`;
    if (minPrice) url += `&min_price=${minPrice}`;
    if (maxPrice) url += `&max_price=${maxPrice}`;
    if (search) url += `&search=${search}`;
    if (sort) url += `&sort=${sort}`;
    
    window.location.href = url;
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Auto-submit filter form on change
document.querySelectorAll('#filter-category, #filter-brand, #filter-sort').forEach(element => {
    element?.addEventListener('change', debounce(function() {
        filterProducts();
    }, 500));
});

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return true;
    
    const inputs = form.querySelectorAll('input, textarea, select');
    let isValid = true;
    
    inputs.forEach(input => {
        if (input.hasAttribute('required') && !input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Format date
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'short', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-IN', options);
}

// Countdown timer for limited offers
function startCountdown(elementId, endTime) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    const timer = setInterval(() => {
        const now = new Date().getTime();
        const distance = new Date(endTime).getTime() - now;
        
        if (distance < 0) {
            element.innerHTML = 'Offer Expired';
            clearInterval(timer);
            return;
        }
        
        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);
        
        element.innerHTML = `${days}d ${hours}h ${minutes}m ${seconds}s`;
    }, 1000);
}

// Copy text to clipboard
function copyToClipboard(text) {
    navigator.clipboard.writeText(text)
        .then(() => showAlert('Copied to clipboard!', 'success'))
        .catch(() => showAlert('Failed to copy', 'error'));
}

// Smooth scroll to element
function smoothScrollTo(elementId) {
    const element = document.getElementById(elementId);
    if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
    }
}

// Toggle dark mode
function toggleDarkMode() {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    document.documentElement.setAttribute('data-theme', isDark ? 'light' : 'dark');
    localStorage.setItem('theme', isDark ? 'light' : 'dark');
}

// Load saved theme
window.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme') || 'light';
    document.documentElement.setAttribute('data-theme', savedTheme);
});

// Logout function
function logout() {
    if (confirm('Are you sure you want to logout?')) {
        window.location.href = '/auth/logout';
    }
}
