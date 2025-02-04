// Function to get a cookie by name
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Function to check if the user is authenticated
function isAuthenticated() {
    const authCookie = getCookie('auth');
    return authCookie !== null;
}

// Example usage
document.addEventListener('DOMContentLoaded', function() {
    if (isAuthenticated()) {
        console.log('User is authenticated');
        // Perform actions for authenticated users
    } else {
        console.log('User is not authenticated');
        // Perform actions for unauthenticated users
    }
});