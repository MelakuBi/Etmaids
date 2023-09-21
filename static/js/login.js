document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('login-form');
    const errorMessage = document.getElementById('error-message');

    loginForm.addEventListener('submit', function(event) {
        event.preventDefault();

        // Reset previous error messages
        resetErrorMessages();

        // Perform login validation here
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        // Example validation - check if email and password are provided
        if (!email) {
            displayError('email', 'Please enter your email address.');
        }
        if (!password) {
            displayError('password', 'Please enter your password.');
        }

        // If any errors exist, prevent form submission
        if (document.querySelectorAll('.error-message:not(:empty)').length > 0) {
            return;
        }

        // Perform login logic here (e.g., check credentials)
        // If login is successful, you can redirect the user to another page.
        // For this example, we'll just display a success message.
        showMessage('Login successful!');
    });
});

function resetErrorMessages() {
    // Reset all error messages to empty
    const errorMessages = document.querySelectorAll('.error-message');
    errorMessages.forEach(function(error) {
        error.textContent = '';
    });
}

function displayError(fieldId, errorMessageText) {
    // Display an error message for the specified field
    const errorField = document.getElementById(`${fieldId}-error`);
    errorField.textContent = errorMessageText;
}

function showMessage(message) {
    // Display a success message
    const errorMessage = document.getElementById('error-message');
    errorMessage.textContent = message;
    errorMessage.style.color = 'green';
}
