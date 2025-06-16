// AutoRent JavaScript Functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initializeFilters();
    initializeDatePickers();
    initializeTooltips();
    initializeAnimations();
    initializeFormValidation();
    initializePriceCalculator();
});

// Filter functionality for car catalog
function initializeFilters() {
    const filterForm = document.querySelector('form[method="get"]');
    if (!filterForm) return;

    // Auto-submit form on filter change
    const filterInputs = filterForm.querySelectorAll('select, input[type="number"]');
    filterInputs.forEach(input => {
        input.addEventListener('change', function() {
            // Add loading state
            const submitBtn = filterForm.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="loading"></span> Поиск...';
                submitBtn.disabled = true;
                
                // Submit form after short delay
                setTimeout(() => {
                    filterForm.submit();
                }, 300);
            }
        });
    });

    // Clear filters functionality
    const clearBtn = filterForm.querySelector('a[href*="car_list"]');
    if (clearBtn) {
        clearBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Clear all form inputs
            filterInputs.forEach(input => {
                if (input.type === 'text' || input.type === 'number') {
                    input.value = '';
                } else if (input.type === 'select-one') {
                    input.selectedIndex = 0;
                }
            });
            
            // Submit form
            filterForm.submit();
        });
    }
}

// Date picker initialization and validation
function initializeDatePickers() {
    const startDateInput = document.getElementById('start_date');
    const endDateInput = document.getElementById('end_date');
    
    if (!startDateInput || !endDateInput) return;

    // Set minimum date to today
    const today = new Date().toISOString().split('T')[0];
    startDateInput.min = today;
    endDateInput.min = today;

    // Update end date minimum when start date changes
    startDateInput.addEventListener('change', function() {
        const startDate = new Date(this.value);
        const nextDay = new Date(startDate);
        nextDay.setDate(startDate.getDate() + 1);
        
        endDateInput.min = nextDay.toISOString().split('T')[0];
        
        // Clear end date if it's before new minimum
        if (endDateInput.value && new Date(endDateInput.value) <= startDate) {
            endDateInput.value = '';
        }
        
        updatePriceCalculation();
    });

    endDateInput.addEventListener('change', updatePriceCalculation);
}

// Price calculation for booking form
function initializePriceCalculator() {
    const startDateInput = document.getElementById('start_date');
    const endDateInput = document.getElementById('end_date');
    
    if (!startDateInput || !endDateInput) return;

    // Create price display element
    const priceDisplay = document.createElement('div');
    priceDisplay.className = 'alert alert-info mt-3';
    priceDisplay.style.display = 'none';
    priceDisplay.innerHTML = '<i class="fas fa-calculator me-2"></i><span id="price-calculation"></span>';
    
    const form = startDateInput.closest('form');
    if (form) {
        form.insertBefore(priceDisplay, form.querySelector('button[type="submit"]'));
    }
}

function updatePriceCalculation() {
    const startDateInput = document.getElementById('start_date');
    const endDateInput = document.getElementById('end_date');
    const priceDisplay = document.querySelector('#price-calculation');
    
    if (!startDateInput || !endDateInput || !priceDisplay) return;
    
    const startDate = startDateInput.value;
    const endDate = endDateInput.value;
    
    if (!startDate || !endDate) {
        priceDisplay.parentElement.style.display = 'none';
        return;
    }
    
    const start = new Date(startDate);
    const end = new Date(endDate);
    const days = Math.ceil((end - start) / (1000 * 60 * 60 * 24));
    
    if (days <= 0) {
        priceDisplay.parentElement.style.display = 'none';
        return;
    }
    
    // Get prices from page (you might need to pass these from Django)
    const pricePerDay = parseFloat(document.querySelector('[data-price-day]')?.dataset.priceDay || 0);
    const pricePerWeek = parseFloat(document.querySelector('[data-price-week]')?.dataset.priceWeek || 0);
    const pricePerMonth = parseFloat(document.querySelector('[data-price-month]')?.dataset.priceMonth || 0);
    
    if (pricePerDay > 0) {
        let totalPrice = 0;
        let priceBreakdown = '';
        
        if (days >= 30 && pricePerMonth > 0) {
            const months = Math.floor(days / 30);
            const remainingDays = days % 30;
            totalPrice = months * pricePerMonth + remainingDays * pricePerDay;
            priceBreakdown = `${months} мес. × ${pricePerMonth.toLocaleString()} ₽ + ${remainingDays} дн. × ${pricePerDay.toLocaleString()} ₽`;
        } else if (days >= 7 && pricePerWeek > 0) {
            const weeks = Math.floor(days / 7);
            const remainingDays = days % 7;
            totalPrice = weeks * pricePerWeek + remainingDays * pricePerDay;
            priceBreakdown = `${weeks} нед. × ${pricePerWeek.toLocaleString()} ₽ + ${remainingDays} дн. × ${pricePerDay.toLocaleString()} ₽`;
        } else {
            totalPrice = days * pricePerDay;
            priceBreakdown = `${days} дн. × ${pricePerDay.toLocaleString()} ₽`;
        }
        
        priceDisplay.innerHTML = `
            <strong>Расчет стоимости:</strong><br>
            ${priceBreakdown}<br>
            <strong>Итого: ${totalPrice.toLocaleString()} ₽</strong>
        `;
        priceDisplay.parentElement.style.display = 'block';
    }
}

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Smooth animations
function initializeAnimations() {
    // Add fade-in animation to cards
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        card.style.animationDelay = `${index * 0.1}s`;
        card.classList.add('fade-in');
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Custom validation for booking form
            if (form.action.includes('add-to-cart')) {
                const startDate = form.querySelector('#start_date')?.value;
                const endDate = form.querySelector('#end_date')?.value;
                
                if (!startDate || !endDate) {
                    e.preventDefault();
                    showAlert('Пожалуйста, выберите даты аренды', 'warning');
                    return;
                }
                
                const start = new Date(startDate);
                const end = new Date(endDate);
                
                if (end <= start) {
                    e.preventDefault();
                    showAlert('Дата окончания должна быть позже даты начала', 'warning');
                    return;
                }
                
                if (start < new Date().setHours(0, 0, 0, 0)) {
                    e.preventDefault();
                    showAlert('Дата начала не может быть в прошлом', 'warning');
                    return;
                }
            }
            
            // Add loading state to submit button
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn && !submitBtn.disabled) {
                const originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="loading"></span> Обработка...';
                submitBtn.disabled = true;
                
                // Re-enable button after 5 seconds (in case of error)
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 5000);
            }
        });
    });
}

// Show alert messages
function showAlert(message, type = 'info') {
    const alertContainer = document.querySelector('.container');
    if (!alertContainer) return;
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.insertBefore(alert, alertContainer.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alert.parentNode) {
            alert.remove();
        }
    }, 5000);
}

// Confirmation dialogs
function confirmAction(message) {
    return confirm(message);
}

// Image lazy loading
function initializeLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Search functionality
function initializeSearch() {
    const searchInput = document.querySelector('input[name="search"]');
    if (!searchInput) return;
    
    let searchTimeout;
    
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        
        searchTimeout = setTimeout(() => {
            if (this.value.length >= 3 || this.value.length === 0) {
                this.form.submit();
            }
        }, 500);
    });
}

// Mobile menu toggle
function initializeMobileMenu() {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (!navbarToggler || !navbarCollapse) return;
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', function(e) {
        if (!navbarCollapse.contains(e.target) && !navbarToggler.contains(e.target)) {
            if (navbarCollapse.classList.contains('show')) {
                navbarToggler.click();
            }
        }
    });
}

// Initialize additional features when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initializeLazyLoading();
    initializeSearch();
    initializeMobileMenu();
});

// Utility functions
function formatPrice(price) {
    return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB',
        minimumFractionDigits: 0
    }).format(price);
}

function formatDate(date) {
    return new Intl.DateTimeFormat('ru-RU').format(new Date(date));
}

// Export functions for global use
window.AutoRent = {
    showAlert,
    confirmAction,
    formatPrice,
    formatDate,
    updatePriceCalculation
};

