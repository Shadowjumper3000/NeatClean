// frontend/src/auth.js

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

function isAuthenticated() {
    const authCookie = getCookie('auth');
    return authCookie !== null;
}

document.addEventListener('DOMContentLoaded', function() {
    if (isAuthenticated()) {
        console.log('User is authenticated');
    } else {
        console.log('User is not authenticated');
    }
});