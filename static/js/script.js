async function generateCode() {
    const generateBtn = document.querySelector('.generate-btn');
    const codeDisplay = document.getElementById('codeDisplay');
    
    generateBtn.classList.add('loading');
    generateBtn.textContent = 'Генерация...';
    
    try {
        const response = await fetch('/generate_code');
        const data = await response.json();
        
        if (response.ok) {
            codeDisplay.textContent = data.code;
            codeDisplay.style.color = '#2ecc71';
        } else {
            throw new Error(data.error || 'Ошибка генерации кода');
        }
    } catch (error) {
        codeDisplay.textContent = 'Ошибка!';
        codeDisplay.style.color = '#e74c3c';
        showError('Ошибка при генерации кода: ' + error.message);
    } finally {
        generateBtn.classList.remove('loading');
        generateBtn.textContent = 'Сгенерировать Код';
    }
}

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error-message';
    errorDiv.textContent = message;
    
    const container = document.querySelector('.generate-section');
    container.appendChild(errorDiv);
    
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

function handleFormSubmit(form) {
    const submitBtn = form.querySelector('button[type="submit"]');
    submitBtn.classList.add('loading');
    submitBtn.textContent = 'Вход...';
    
    return true;
}

document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            handleFormSubmit(this);
        });
    });
});