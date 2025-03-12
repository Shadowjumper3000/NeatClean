document.addEventListener('DOMContentLoaded', function() {

    // Wait for a short moment to ensure all scripts are loaded
    setTimeout(() => {
        const datePickerElement = document.getElementById('date-picker');

        if (datePickerElement && typeof flatpickr === 'function') {

            const datePicker = flatpickr("#date-picker", {
                enableTime: true,
                dateFormat: "F j, Y at h:i K",
                minDate: "today",
                maxDate: new Date().fp_incr(30),
                inline: true,
                disable: [
                    function (date) {
                        return date.getDay() === 0;
                    }
                ],
                locale: {
                    firstDayOfWeek: 1
                },
                minTime: "08:00",
                maxTime: "18:00",
                minuteIncrement: 30,
                defaultHour: 12,
                time_24hr: true,
                altInput: true,
                altFormat: "F j, Y at h:i K",
                onChange: function (selectedDates, dateStr) {
                    const checkButton = document.getElementById('check-availability-button');
                    if (checkButton) {
                        checkButton.style.display = 'block';
                    }
                }
            });

            // Handle availability check
            const checkButton = document.getElementById('check-availability-button');
            if (checkButton) {
                checkButton.addEventListener('click', function () {
                    const selectedDate = datePicker.selectedDates[0];

                    if (selectedDate) {
                        const dateParam = selectedDate.toISOString().split('T')[0];
                        const timeParam = selectedDate.toTimeString().slice(0, 5);

                        const url = new URL("/staff-list/", window.location.origin);
                        url.searchParams.append('date', dateParam);
                        url.searchParams.append('time', timeParam);
                        window.location.href = url.toString();
                    }
                });
            }
        } else {
            console.warn('Date picker element not found or flatpickr not loaded');
        }
    }, 100);
});