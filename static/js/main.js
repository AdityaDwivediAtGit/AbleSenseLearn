// AbleSense Learn - Main JavaScript File

// Document Ready Function
document.addEventListener('DOMContentLoaded', function() {
    console.log('AbleSense Learn loaded');
    
    // Initialize components
    initializeAccessibility();
    initializeNavigation();
    initializeForms();
    initializeInteractiveElements();
    initializeKeyboardShortcuts();
    
    // Load user preferences
    loadUserPreferences();
    
    // Check for accessibility features
    checkAccessibilitySupport();
});

// Accessibility Initialization
function initializeAccessibility() {
    // Add skip link if not present
    if (!document.querySelector('.skip-to-main')) {
        const skipLink = document.createElement('a');
        skipLink.href = '#main-content';
        skipLink.className = 'skip-to-main';
        skipLink.textContent = 'Skip to main content';
        document.body.insertBefore(skipLink, document.body.firstChild);
    }
    
    // Ensure all interactive elements are focusable
    makeInteractiveElementsFocusable();
    
    // Initialize ARIA attributes
    initializeAriaAttributes();
    
    // Set up focus trapping for modals
    setupFocusTrapping();
}

// Make all interactive elements focusable
function makeInteractiveElementsFocusable() {
    const interactiveSelectors = [
        'button:not([disabled])',
        'a[href]',
        'input:not([disabled])',
        'select:not([disabled])',
        'textarea:not([disabled])',
        '[tabindex]',
        '[contenteditable]'
    ];
    
    const interactiveElements = document.querySelectorAll(interactiveSelectors.join(', '));
    
    interactiveElements.forEach(element => {
        if (!element.hasAttribute('tabindex')) {
            element.setAttribute('tabindex', '0');
        }
    });
}

// Initialize ARIA attributes
function initializeAriaAttributes() {
    // Add aria-label to buttons without text
    document.querySelectorAll('button:not([aria-label]):empty').forEach(button => {
        const icon = button.querySelector('i, svg, img');
        if (icon) {
            button.setAttribute('aria-label', button.title || 'Button');
        }
    });
    
    // Add aria-describedby to form controls with error messages
    document.querySelectorAll('.form-control').forEach(input => {
        const errorMessage = input.nextElementSibling;
        if (errorMessage && errorMessage.classList.contains('error-message')) {
            const errorId = 'error-' + input.id;
            errorMessage.id = errorId;
            input.setAttribute('aria-describedby', errorId);
        }
    });
    
    // Add aria-live regions for dynamic content
    const liveRegion = document.createElement('div');
    liveRegion.setAttribute('aria-live', 'polite');
    liveRegion.setAttribute('aria-atomic', 'true');
    liveRegion.className = 'sr-only';
    liveRegion.id = 'live-region';
    document.body.appendChild(liveRegion);
}

// Setup focus trapping for modals
function setupFocusTrapping() {
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Tab' && document.querySelector('.modal.show')) {
            trapFocus(event);
        }
    });
}

function trapFocus(event) {
    const modal = document.querySelector('.modal.show');
    if (!modal) return;
    
    const focusableElements = modal.querySelectorAll(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
    );
    
    if (focusableElements.length === 0) return;
    
    const firstElement = focusableElements[0];
    const lastElement = focusableElements[focusableElements.length - 1];
    
    if (event.shiftKey && document.activeElement === firstElement) {
        lastElement.focus();
        event.preventDefault();
    } else if (!event.shiftKey && document.activeElement === lastElement) {
        firstElement.focus();
        event.preventDefault();
    }
}

// Navigation Initialization
function initializeNavigation() {
    // Handle mobile menu toggle
    const menuToggle = document.querySelector('.menu-toggle');
    if (menuToggle) {
        menuToggle.addEventListener('click', toggleMobileMenu);
        menuToggle.addEventListener('keydown', function(event) {
            if (event.key === 'Enter' || event.key === ' ') {
                toggleMobileMenu();
                event.preventDefault();
            }
        });
    }
    
    // Handle dropdown menus
    document.querySelectorAll('.has-dropdown').forEach(dropdown => {
        const toggle = dropdown.querySelector('.dropdown-toggle');
        const menu = dropdown.querySelector('.dropdown-menu');
        
        if (toggle && menu) {
            toggle.addEventListener('click', function(event) {
                event.stopPropagation();
                toggleDropdown(this);
            });
            
            toggle.addEventListener('keydown', function(event) {
                if (event.key === 'Enter' || event.key === ' ') {
                    event.preventDefault();
                    toggleDropdown(this);
                } else if (event.key === 'Escape') {
                    closeDropdown(this);
                } else if (event.key === 'ArrowDown') {
                    event.preventDefault();
                    openDropdown(this);
                    focusFirstMenuItem(menu);
                }
            });
            
            // Close dropdown when clicking outside
            document.addEventListener('click', function() {
                closeDropdown(toggle);
            });
        }
    });
    
    // Handle current page highlighting
    highlightCurrentPage();
}

function toggleMobileMenu() {
    const nav = document.querySelector('.main-nav');
    const toggle = document.querySelector('.menu-toggle');
    
    if (nav && toggle) {
        const isExpanded = nav.classList.toggle('show');
        toggle.setAttribute('aria-expanded', isExpanded);
        
        if (isExpanded) {
            // Focus first nav item when menu opens
            const firstNavItem = nav.querySelector('a, button');
            if (firstNavItem) firstNavItem.focus();
        }
    }
}

function toggleDropdown(toggle) {
    const isExpanded = toggle.getAttribute('aria-expanded') === 'true';
    if (isExpanded) {
        closeDropdown(toggle);
    } else {
        openDropdown(toggle);
    }
}

function openDropdown(toggle) {
    toggle.setAttribute('aria-expanded', 'true');
    const menu = toggle.nextElementSibling;
    if (menu && menu.classList.contains('dropdown-menu')) {
        menu.classList.add('show');
    }
}

function closeDropdown(toggle) {
    toggle.setAttribute('aria-expanded', 'false');
    const menu = toggle.nextElementSibling;
    if (menu && menu.classList.contains('dropdown-menu')) {
        menu.classList.remove('show');
    }
}

function focusFirstMenuItem(menu) {
    const firstItem = menu.querySelector('a, button');
    if (firstItem) firstItem.focus();
}

function highlightCurrentPage() {
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
            link.setAttribute('aria-current', 'page');
        }
    });
}

// Forms Initialization
function initializeForms() {
    // Add form validation
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', handleFormSubmit);
        
        // Real-time validation
        form.querySelectorAll('.form-control').forEach(input => {
            input.addEventListener('blur', validateField);
            input.addEventListener('input', clearFieldError);
        });
    });
    
    // Handle password visibility toggle
    document.querySelectorAll('.toggle-password').forEach(toggle => {
        toggle.addEventListener('click', function() {
            togglePasswordVisibility(this);
        });
    });
}

function handleFormSubmit(event) {
    const form = event.target;
    let isValid = true;
    
    // Validate all fields
    form.querySelectorAll('.form-control[required]').forEach(input => {
        if (!validateField({ target: input })) {
            isValid = false;
        }
    });
    
    if (!isValid) {
        event.preventDefault();
        
        // Focus first invalid field
        const firstInvalid = form.querySelector('.form-control.error');
        if (firstInvalid) {
            firstInvalid.focus();
            announceToScreenReader('Please check the form for errors.');
        }
    }
}

function validateField(event) {
    const input = event.target;
    const value = input.value.trim();
    let isValid = true;
    let errorMessage = '';
    
    // Clear previous error
    clearFieldError({ target: input });
    
    // Required field validation
    if (input.hasAttribute('required') && !value) {
        isValid = false;
        errorMessage = 'This field is required.';
    }
    
    // Email validation
    if (input.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            isValid = false;
            errorMessage = 'Please enter a valid email address.';
        }
    }
    
    // Password validation
    if (input.type === 'password' && value) {
        if (value.length < 8) {
            isValid = false;
            errorMessage = 'Password must be at least 8 characters.';
        }
    }
    
    // Custom validation
    const pattern = input.getAttribute('pattern');
    if (pattern && value) {
        const regex = new RegExp(pattern);
        if (!regex.test(value)) {
            isValid = false;
            errorMessage = input.getAttribute('data-pattern-error') || 'Invalid format.';
        }
    }
    
    // Show error or success
    if (!isValid) {
        showFieldError(input, errorMessage);
    } else if (value) {
        showFieldSuccess(input);
    }
    
    return isValid;
}

function showFieldError(input, message) {
    input.classList.add('error');
    input.classList.remove('success');
    
    const errorElement = document.createElement('span');
    errorElement.className = 'error-message';
    errorElement.textContent = message;
    
    input.parentNode.appendChild(errorElement);
    input.setAttribute('aria-invalid', 'true');
}

function showFieldSuccess(input) {
    input.classList.add('success');
    input.classList.remove('error');
    input.setAttribute('aria-invalid', 'false');
}

function clearFieldError(event) {
    const input = event.target;
    input.classList.remove('error', 'success');
    input.removeAttribute('aria-invalid');
    
    const errorElement = input.parentNode.querySelector('.error-message');
    const successElement = input.parentNode.querySelector('.success-message');
    
    if (errorElement) errorElement.remove();
    if (successElement) successElement.remove();
}

function togglePasswordVisibility(toggle) {
    const input = toggle.previousElementSibling;
    if (input && input.type === 'password') {
        input.type = 'text';
        toggle.textContent = 'Hide';
        toggle.setAttribute('aria-label', 'Hide password');
    } else if (input && input.type === 'text') {
        input.type = 'password';
        toggle.textContent = 'Show';
        toggle.setAttribute('aria-label', 'Show password');
    }
}

// Interactive Elements
function initializeInteractiveElements() {
    // Handle card interactions
    document.querySelectorAll('.card').forEach(card => {
        card.addEventListener('keydown', function(event) {
            if (event.key === 'Enter' || event.key === ' ') {
                event.preventDefault();
                const link = this.querySelector('a[href]');
                if (link) link.click();
            }
        });
    });
    
    // Handle loading states
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function() {
            if (this.classList.contains('btn-loading')) {
                this.classList.add('loading');
                this.setAttribute('aria-busy', 'true');
            }
        });
    });
    
    // Handle dismissible alerts
    document.querySelectorAll('.alert-dismissible .close').forEach(closeBtn => {
        closeBtn.addEventListener('click', function() {
            const alert = this.closest('.alert');
            if (alert) {
                alert.style.transition = 'opacity 0.3s';
                alert.style.opacity = '0';
                setTimeout(() => alert.remove(), 300);
            }
        });
    });
}

// Keyboard Shortcuts
function initializeKeyboardShortcuts() {
    document.addEventListener('keydown', function(event) {
        // Skip if user is typing in an input
        if (event.target.matches('input, textarea, select, [contenteditable]')) {
            return;
        }
        
        // Accessibility shortcuts
        switch(event.key) {
            case '1':
                if (event.altKey) {
                    event.preventDefault();
                    document.getElementById('main-content')?.focus();
                }
                break;
                
            case '2':
                if (event.altKey) {
                    event.preventDefault();
                    document.querySelector('nav')?.focus();
                }
                break;
                
            case 'h':
                if (event.ctrlKey) {
                    event.preventDefault();
                    toggleHighContrast();
                }
                break;
                
            case 'd':
                if (event.ctrlKey) {
                    event.preventDefault();
                    toggleDyslexiaMode();
                }
                break;
                
            case 'm':
                if (event.ctrlKey) {
                    event.preventDefault();
                    toggleTextSize();
                }
                break;
                
            case 'Escape':
                // Close all modals and dropdowns
                document.querySelectorAll('.modal.show, .dropdown-menu.show').forEach(element => {
                    element.classList.remove('show');
                });
                document.querySelectorAll('[aria-expanded="true"]').forEach(element => {
                    element.setAttribute('aria-expanded', 'false');
                });
                break;
        }
    });
}

// User Preferences
function loadUserPreferences() {
    const preferences = JSON.parse(localStorage.getItem('ablelearn_preferences') || '{}');
    
    // Apply saved preferences
    if (preferences.highContrast) {
        document.documentElement.classList.add('high-contrast');
    }
    
    if (preferences.dyslexiaMode) {
        document.documentElement.classList.add('dyslexia-friendly');
    }
    
    if (preferences.largeText) {
        document.documentElement.classList.add('large-text');
    }
    
    if (preferences.reducedMotion) {
        document.documentElement.classList.add('reduced-motion');
    }
    
    // Update UI to reflect saved preferences
    updatePreferenceUI(preferences);
}

function saveUserPreferences(preferences) {
    const current = JSON.parse(localStorage.getItem('ablelearn_preferences') || '{}');
    const updated = { ...current, ...preferences };
    localStorage.setItem('ablelearn_preferences', JSON.stringify(updated));
    loadUserPreferences();
}

function updatePreferenceUI(preferences) {
    // Update toggle buttons based on preferences
    document.querySelectorAll('[data-preference]').forEach(toggle => {
        const preference = toggle.dataset.preference;
        const isActive = preferences[preference];
        
        toggle.classList.toggle('active', isActive);
        toggle.setAttribute('aria-pressed', isActive);
    });
}

// Accessibility Features
function toggleHighContrast() {
    document.documentElement.classList.toggle('high-contrast');
    const isActive = document.documentElement.classList.contains('high-contrast');
    
    saveUserPreferences({ highContrast: isActive });
    announceToScreenReader(`High contrast mode ${isActive ? 'enabled' : 'disabled'}`);
}

function toggleDyslexiaMode() {
    document.documentElement.classList.toggle('dyslexia-friendly');
    const isActive = document.documentElement.classList.contains('dyslexia-friendly');
    
    saveUserPreferences({ dyslexiaMode: isActive });
    announceToScreenReader(`Dyslexia-friendly mode ${isActive ? 'enabled' : 'disabled'}`);
}

function toggleTextSize() {
    const hasLarge = document.documentElement.classList.contains('large-text');
    const hasXLarge = document.documentElement.classList.contains('xlarge-text');
    
    if (!hasLarge && !hasXLarge) {
        document.documentElement.classList.add('large-text');
        saveUserPreferences({ largeText: true, xlargeText: false });
        announceToScreenReader('Large text enabled');
    } else if (hasLarge && !hasXLarge) {
        document.documentElement.classList.remove('large-text');
        document.documentElement.classList.add('xlarge-text');
        saveUserPreferences({ largeText: false, xlargeText: true });
        announceToScreenReader('Extra large text enabled');
    } else {
        document.documentElement.classList.remove('xlarge-text');
        saveUserPreferences({ largeText: false, xlargeText: false });
        announceToScreenReader('Normal text size restored');
    }
}

function toggleReducedMotion() {
    document.documentElement.classList.toggle('reduced-motion');
    const isActive = document.documentElement.classList.contains('reduced-motion');
    
    saveUserPreferences({ reducedMotion: isActive });
    announceToScreenReader(`Reduced motion ${isActive ? 'enabled' : 'disabled'}`);
}

// Utility Functions
function announceToScreenReader(message) {
    const liveRegion = document.getElementById('live-region');
    if (liveRegion) {
        liveRegion.textContent = message;
        
        // Clear after announcement
        setTimeout(() => {
            liveRegion.textContent = '';
        }, 1000);
    }
}

function checkAccessibilitySupport() {
    // Check for prefers-reduced-motion
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReducedMotion) {
        document.documentElement.classList.add('reduced-motion');
    }
    
    // Check for prefers-color-scheme
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (prefersDark) {
        document.documentElement.classList.add('dark-mode');
    }
    
    // Check for browser support of :focus-visible
    try {
        document.querySelector(':focus-visible');
    } catch (e) {
        // Polyfill :focus-visible if needed
        importFocusVisiblePolyfill();
    }
}

async function importFocusVisiblePolyfill() {
    try {
        const { applyFocusVisiblePolyfill } = await import('https://unpkg.com/focus-visible@5.2.0/dist/focus-visible.min.js');
        applyFocusVisiblePolyfill();
    } catch (error) {
        console.warn('Could not load focus-visible polyfill:', error);
    }
}

// API Integration
async function simplifyText(text, level = 'intermediate') {
    try {
        const response = await fetch('/api/content/simplify', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text, level })
        });
        
        if (!response.ok) throw new Error('API request failed');
        
        return await response.json();
    } catch (error) {
        console.error('Text simplification failed:', error);
        return { simplified: text, error: true };
    }
}

async function describeImage(imageFile) {
    try {
        const formData = new FormData();
        formData.append('image', imageFile);
        
        const response = await fetch('/api/image/describe', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) throw new Error('API request failed');
        
        return await response.json();
    } catch (error) {
        console.error('Image description failed:', error);
        return { description: 'Unable to describe image', error: true };
    }
}

// Export for use in other modules
window.AbleSenseLearn = {
    simplifyText,
    describeImage,
    toggleHighContrast,
    toggleDyslexiaMode,
    toggleTextSize,
    toggleReducedMotion,
    announceToScreenReader
};