function updateBookingStatus(bookingId, status) {

    // Get CSRF token
    const csrftoken = getCookie('csrftoken');

    fetch(`/api/bookings/${bookingId}/status/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({ status: status })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Reload the page to show updated status
        window.location.reload();
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to update booking status');
    });
}

// Helper function to get CSRF token
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

function openChat(userId) {
    console.log('Opening chat with user:', userId);
    // TODO: Implement chat functionality
    alert('Chat feature coming soon!');
}