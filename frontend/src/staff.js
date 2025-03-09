document.addEventListener('DOMContentLoaded', function() {
    // Initialize date picker for staff
    flatpickr("#availability-date", {
        dateFormat: "Y-m-d",
        mode: "multiple",
        minDate: "today",
        maxDate: new Date().fp_incr(60), // Set availability up to 60 days ahead
        locale: {
            firstDayOfWeek: 1
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
});