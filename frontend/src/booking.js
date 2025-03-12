function bookCleaner(staffId) {
    const date = document.getElementById('date').value;
    const time = document.getElementById('time').value;

    // Fetch user's address from their profile
    function formatAddress(user) {
        const parts = [];
        if (user.street && user.street_number) {
            parts.push(`${user.street} ${user.street_number}`);
        }
        if (user.apartment) {
            parts.push(`Apt ${user.apartment}`);
        }
        if (user.city) {
            parts.push(user.city);
        }
        if (user.state) {
            parts.push(user.state);
        }
        if (user.zip_code) {
            parts.push(user.zip_code);
        }
        if (user.country) {
            parts.push(user.country);
        }
        return parts.join(', ');
    }

    // First fetch the user's profile data
    fetch('/api/user/profile/', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(response => response.json())
    .then(userData => {
        const address = formatAddress(userData);

        if (!address || !date || !time) {
            alert('Please provide all required information');
            return;
        }

        const bookingData = {
            staff_id: staffId,
            date: date,
            time: time,
            address: address
        };

        // Create the booking
        return fetch('/api/bookings/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(bookingData)
        });
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        alert("Booking saved! You can check the status on the bookings page.");
        window.location.href = "/bookings/";
    })
    .catch(error => {
        console.error('Error:', error);
        alert("An error occurred. Please try again.");
    });
}

// Function to get CSRF token
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
