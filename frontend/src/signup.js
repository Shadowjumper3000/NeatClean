// frontend/src/signup.js

document.addEventListener('DOMContentLoaded', function() {
    const signupForm = document.getElementById('signup-form');

    signupForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(signupForm);

        // Debugging: Log form data
        for (let [key, value] of formData.entries()) {
            console.log(`${key}: ${value}`);
        }

        fetch('/register/', {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: formData
        })
        .then(response => {
            // Debugging: Log response status and headers
            console.log('Response status:', response.status);
            console.log('Response headers:', response.headers);
            return response.json();
        })
        .then(data => {
            // Debugging: Log response data
            console.log('Response data:', data);
            if (data.success) {
                window.location.href = '/account/';
            } else {
                alert(JSON.stringify(data.error));
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});

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