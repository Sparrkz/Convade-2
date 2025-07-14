// Main JavaScript file for Convade LMS

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
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

    // Form validation feedback
    const forms = document.querySelectorAll('.needs-validation');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', event => {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
});

// Django CSRF token handling
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Set CSRF token for all AJAX requests
const csrftoken = getCookie('csrftoken');
if (csrftoken) {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!this.crossDomain && ['POST', 'PUT', 'DELETE', 'PATCH'].includes(settings.type)) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
            }
        }
    });
}

// Course enrollment functionality
function enrollInCourse(courseId) {
    $.ajax({
        url: `/courses/${courseId}/enroll/`,
        method: 'POST',
        data: {
            'csrfmiddlewaretoken': csrftoken
        },
        success: function(response) {
            if (response.success) {
                showNotification('Successfully enrolled in course!', 'success');
                location.reload();
            } else {
                showNotification(response.message || 'Enrollment failed', 'error');
            }
        },
        error: function() {
            showNotification('An error occurred during enrollment', 'error');
        }
    });
}

// Test timer functionality
let testTimer = null;
let timeRemaining = 0;

function startTestTimer(duration) {
    timeRemaining = duration;
    const timerDisplay = document.getElementById('test-timer');
    
    testTimer = setInterval(function() {
        const hours = Math.floor(timeRemaining / 3600);
        const minutes = Math.floor((timeRemaining % 3600) / 60);
        const seconds = timeRemaining % 60;
        
        timerDisplay.innerHTML = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
        
        if (timeRemaining <= 0) {
            clearInterval(testTimer);
            submitTest();
        }
        
        timeRemaining--;
    }, 1000);
}

function submitTest() {
    const form = document.getElementById('test-form');
    if (form) {
        form.submit();
    }
}

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('is-invalid');
            isValid = false;
        } else {
            input.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// Notification system
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

// Progress tracking
function updateProgress(courseId, contentId) {
    $.ajax({
        url: `/courses/${courseId}/progress/`,
        method: 'POST',
        data: {
            'content_id': contentId,
            'csrfmiddlewaretoken': csrftoken
        },
        success: function(response) {
            if (response.progress) {
                updateProgressBar(response.progress);
            }
        }
    });
}

function updateProgressBar(progress) {
    const progressBar = document.querySelector('.progress-bar');
    if (progressBar) {
        progressBar.style.width = progress + '%';
        progressBar.setAttribute('aria-valuenow', progress);
        progressBar.textContent = Math.round(progress) + '%';
    }
}

// Search functionality
function initializeSearch() {
    const searchForm = document.getElementById('search-form');
    const searchInput = document.getElementById('search-input');
    
    if (searchForm && searchInput) {
        searchForm.addEventListener('submit', function(e) {
            if (!searchInput.value.trim()) {
                e.preventDefault();
                showNotification('Please enter a search term', 'warning');
            }
        });
    }
}

// Badge animation
function animateBadge(badgeElement) {
    badgeElement.classList.add('animate__animated', 'animate__bounceIn');
    setTimeout(() => {
        badgeElement.classList.remove('animate__animated', 'animate__bounceIn');
    }, 1000);
}

// Course rating
function rateCourse(courseId, rating) {
    $.ajax({
        url: `/courses/${courseId}/rate/`,
        method: 'POST',
        data: {
            'rating': rating,
            'csrfmiddlewaretoken': csrftoken
        },
        success: function(response) {
            if (response.success) {
                showNotification('Thank you for rating this course!', 'success');
                updateStarRating(rating);
            }
        }
    });
}

function updateStarRating(rating) {
    const stars = document.querySelectorAll('.star-rating .star');
    stars.forEach((star, index) => {
        if (index < rating) {
            star.classList.add('active');
        } else {
            star.classList.remove('active');
        }
    });
}

// Certificate download
function downloadCertificate(certificateId) {
    window.open(`/certificates/${certificateId}/download/`, '_blank');
}

// Video player controls
function initializeVideoPlayer() {
    const videoPlayers = document.querySelectorAll('.course-video');
    
    videoPlayers.forEach(player => {
        player.addEventListener('ended', function() {
            const courseId = this.dataset.courseId;
            const contentId = this.dataset.contentId;
            if (courseId && contentId) {
                updateProgress(courseId, contentId);
            }
        });
    });
}

// Live chat functionality
function initializeLiveChat() {
    const chatToggle = document.getElementById('chat-toggle');
    const chatWindow = document.getElementById('chat-window');
    
    if (chatToggle && chatWindow) {
        chatToggle.addEventListener('click', function() {
            chatWindow.classList.toggle('d-none');
        });
    }
}

// Auto-save form data
function autoSaveForm(formId, interval = 30000) {
    const form = document.getElementById(formId);
    if (!form) return;
    
    setInterval(() => {
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        localStorage.setItem(`autosave_${formId}`, JSON.stringify(data));
    }, interval);
}

function restoreFormData(formId) {
    const savedData = localStorage.getItem(`autosave_${formId}`);
    if (savedData) {
        const data = JSON.parse(savedData);
        const form = document.getElementById(formId);
        
        Object.keys(data).forEach(key => {
            const input = form.querySelector(`[name="${key}"]`);
            if (input) {
                input.value = data[key];
            }
        });
    }
}

// Initialize everything when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    initializeSearch();
    initializeVideoPlayer();
    initializeLiveChat();
    
    // Initialize star ratings
    const starRatings = document.querySelectorAll('.star-rating');
    starRatings.forEach(rating => {
        const stars = rating.querySelectorAll('.star');
        stars.forEach((star, index) => {
            star.addEventListener('click', function() {
                const courseId = rating.dataset.courseId;
                if (courseId) {
                    rateCourse(courseId, index + 1);
                }
            });
        });
    });
    
    // Initialize enrollment buttons
    const enrollButtons = document.querySelectorAll('.enroll-btn');
    enrollButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            const courseId = this.dataset.courseId;
            if (courseId) {
                enrollInCourse(courseId);
            }
        });
    });
    
    // Initialize test timer if on test page
    const timerElement = document.getElementById('test-timer');
    if (timerElement && timerElement.dataset.duration) {
        startTestTimer(parseInt(timerElement.dataset.duration));
    }
    
    // Initialize form auto-save for test forms
    const testForm = document.getElementById('test-form');
    if (testForm) {
        autoSaveForm('test-form');
        restoreFormData('test-form');
    }
});

// Export functions for external use
window.ConvadeLMS = {
    enrollInCourse,
    startTestTimer,
    submitTest,
    validateForm,
    showNotification,
    updateProgress,
    rateCourse,
    downloadCertificate,
    animateBadge
}; 