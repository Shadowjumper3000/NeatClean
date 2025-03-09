document.addEventListener('DOMContentLoaded', function() {
    // Initialize date picker
    const datePicker = flatpickr("#date-picker", {
        enableTime: true,
        dateFormat: "F j, Y at h:i K", // Example: "March 15, 2025 at 2:30 PM"
        minDate: "today",
        maxDate: new Date().fp_incr(30),
        inline: true,
        static: true,
        disable: [
            function(date) {
                return date.getDay() === 0; // Disable Sundays
            }
        ],
        locale: {
            firstDayOfWeek: 1
        },
        minTime: "08:00",
        maxTime: "18:00",
        minuteIncrement: 30,
        defaultHour: 12,
        time_24hr: false,
        altInput: true,
        altFormat: "F j, Y at h:i K",
        onChange: function(selectedDates, dateStr, instance) {
            console.log('Selected datetime:', dateStr);
        }
    });

    // Handle availability check
    document.getElementById('check-availability-button').addEventListener('click', function() {
        const selectedDate = datePicker.selectedDates[0];

        if (selectedDate) {
            // Format date for URL parameters
            const dateParam = selectedDate.toISOString().split('T')[0];
            const timeParam = selectedDate.toTimeString().slice(0, 5);

            const url = new URL("/staff-list/", window.location.origin);
            url.searchParams.append('date', dateParam);
            url.searchParams.append('time', timeParam);
            window.location.href = url.toString();
        } else {
            alert('Please select a date and time.');
        }
    });
});