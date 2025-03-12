document.addEventListener('DOMContentLoaded', function() {
    // Initialize date picker for staff
    flatpickr("#availability-date", {
        dateFormat: "Y-m-d",
        mode: "multiple",
        minDate: "today",
        maxDate: new Date().fp_incr(60), // Set availability up to 60 days ahead
        locale: {
            firstDayOfWeek: 1
        },
        onChange: function(selectedDates, dateStr) {
        }
    });

    // Initialize time pickers for staff
    flatpickr("#start-time", {
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i",
        minTime: "06:00",
        maxTime: "20:00",
        defaultHour: 8,
        minuteIncrement: 30
    });

    flatpickr("#end-time", {
        enableTime: true,
        noCalendar: true,
        dateFormat: "H:i",
        minTime: "06:00",
        maxTime: "20:00",
        defaultHour: 17,
        minuteIncrement: 30
    });

    // Handle save availability
    document.getElementById('save-availability').addEventListener('click', function() {
        const dates = document.getElementById('availability-date').value;
        const startTime = document.getElementById('start-time').value;
        const endTime = document.getElementById('end-time').value;

        if (!dates || !startTime || !endTime) {
            alert('Please select dates and times');
            return;
        }

        fetch('/api/availability/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                dates: dates,
                startTime: startTime,
                endTime: endTime
            })
        })
        .then(response => response.json())
        .then(data => {
            alert('Availability saved successfully!');
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Failed to save availability');
        });
    });
});