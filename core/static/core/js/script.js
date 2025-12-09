document.addEventListener('DOMContentLoaded', function() {
    
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('error');
                    field.style.borderColor = 'red';
                } else {
                    field.classList.remove('error');
                    field.style.borderColor = '';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields');
            }
        });
    });
    
    const completionCheckboxes = document.querySelectorAll('.completion-toggle');
    completionCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const assignmentRow = this.closest('tr') || this.closest('.assignment-item');
            if (this.checked) {
                assignmentRow.classList.add('completed');
                assignmentRow.style.opacity = '0.6';
                assignmentRow.style.textDecoration = 'line-through';
            } else {
                assignmentRow.classList.remove('completed');
                assignmentRow.style.opacity = '1';
                assignmentRow.style.textDecoration = 'none';
            }
        });
    });
    
    const deleteButtons = document.querySelectorAll('.delete-btn');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this?')) {
                e.preventDefault();
            }
        });
    });
    
    const searchInput = document.querySelector('#course-search');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            const courseItems = document.querySelectorAll('.course-item');
            
            courseItems.forEach(item => {
                const courseName = item.querySelector('.course-name')?.textContent.toLowerCase() || '';
                const courseCode = item.querySelector('.course-code')?.textContent.toLowerCase() || '';
                
                if (courseName.includes(searchTerm) || courseCode.includes(searchTerm)) {
                    item.style.display = '';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    }
    
    function calculateTotalStudyTime() {
        const durationElements = document.querySelectorAll('.study-duration');
        let totalMinutes = 0;
        
        durationElements.forEach(el => {
            const duration = parseFloat(el.textContent) || 0;
            totalMinutes += duration;
        });
        
        const hours = Math.floor(totalMinutes / 60);
        const minutes = totalMinutes % 60;
        
        const totalDisplay = document.querySelector('#total-study-time');
        if (totalDisplay) {
            totalDisplay.textContent = `${hours}h ${minutes}m`;
        }
    }
    
    calculateTotalStudyTime();
    
    const courseSelect = document.querySelector('#id_course');
    const assignmentSelect = document.querySelector('#id_assignment');
    
    if (courseSelect && assignmentSelect) {
        const allAssignments = Array.from(assignmentSelect.options);
        
        courseSelect.addEventListener('change', function() {
            const selectedCourseId = this.value;
            
            assignmentSelect.innerHTML = '<option value="">-- Select Assignment (Optional) --</option>';
            
            allAssignments.forEach(option => {
                if (option.dataset.courseId === selectedCourseId || !selectedCourseId) {
                    assignmentSelect.appendChild(option.cloneNode(true));
                }
            });
        });
    }
    
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
    
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    
    const assignmentDates = document.querySelectorAll('.due-date');
    assignmentDates.forEach(dateEl => {
        const dueDate = new Date(dateEl.textContent);
        const assignmentRow = dateEl.closest('tr') || dateEl.closest('.assignment-item');
        const isCompleted = assignmentRow?.querySelector('.completion-toggle')?.checked;
        
        if (dueDate < today && !isCompleted) {
            dateEl.style.color = 'red';
            dateEl.style.fontWeight = 'bold';
            assignmentRow?.classList.add('overdue');
        } else if (dueDate <= new Date(today.getTime() + 3 * 24 * 60 * 60 * 1000) && !isCompleted) {
            dateEl.style.color = 'orange';
            assignmentRow?.classList.add('upcoming');
        }
    });
    
    const textareas = document.querySelectorAll('textarea');
    textareas.forEach(textarea => {
        let timeout;
        textarea.addEventListener('input', function() {
            clearTimeout(timeout);
            const saveIndicator = document.createElement('span');
            saveIndicator.textContent = ' (unsaved changes)';
            saveIndicator.style.color = 'orange';
            saveIndicator.style.fontSize = '12px';
            
            const existingIndicator = this.parentElement.querySelector('.save-indicator');
            if (existingIndicator) {
                existingIndicator.remove();
            }
            
            saveIndicator.classList.add('save-indicator');
            this.parentElement.appendChild(saveIndicator);
        });
    });
    
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
        });
    }
});

function formatDuration(minutes) {
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return `${hours}h ${mins}m`;
}

function showNotification(message, type = 'success') {
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background: ${type === 'success' ? '#28a745' : '#dc3545'};
        color: white;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
        z-index: 9999;
        animation: slideIn 0.3s ease;
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}