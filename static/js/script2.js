document.addEventListener('DOMContentLoaded', function() {
    const registrationForm = document.getElementById('registration-form');
    const errorMessage = document.getElementById('error-message');

    registrationForm.addEventListener('submit', function(event) {
        event.preventDefault();

        // Reset previous error messages
        resetErrorMessages();

        // Perform form validation here
        const userType = document.querySelector('input[name="user-type"]:checked');
        const firstName = document.getElementById('first-name').value;
        const lastName = document.getElementById('last-name').value;
        const username = document.getElementById('user-name').value;
        //const email = document.getElementById('email').value;
        const phone = document.getElementById('phone').value;
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm-password').value;
       // const photo = document.getElementById('profilePicture').value;
       function phonenumber(phone)
       {
        const regex = /^0[79]\d{8}$/;
         if(regex.test(phone))
               {
             return true;
               }
             else
               {
               return false;
               }
       }
        // Check if any of the fields are empty and display errors
       if (!userType) {
            displayError('user-type', 'Please select a user type.');
        } 
        if (!firstName) {
            displayError('first-name', 'Please enter your first name.');
        }
        if (!lastName) {
            displayError('last-name', 'Please enter your last name.');
        }
        if (!username) {
            displayError('user-name', 'Please fill user name.');
        }
      /*  if (!email) {
            displayError('email', 'Please enter your email address.');
        } */
        if (!phone) {
            displayError('phone', 'Please enter your phone number.');
        } else if (phonenumber(phone) !== true) {
            displayError('phone', 'Invalid phone number.')
        }

        if (!password) {
            displayError('password', 'Please enter a password.');
        }
        if (!confirmPassword) {
            displayError('confirm-password', 'Please confirm your password.');
        }
       /* if (!photo) {
            displayError('photo', 'Please upload your photo.');
        } */
        // Check if passwords match and display an error if they don't
        if (password !== confirmPassword) {
            displayError('confirm-password', 'Passwords do not match.');
        }

        // If any errors exist, prevent form submission
        if (document.querySelectorAll('.error-message:not(:empty)').length > 0) {
            return;
        }

        // Submit the form if validation passes
               registrationForm.submit();

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

