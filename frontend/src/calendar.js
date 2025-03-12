document.addEventListener('DOMContentLoaded', function() {
    console.log('Calendar script loaded');

    // Wait for a short moment to ensure all scripts are loaded
    setTimeout(() => {
        const datePickerElement = document.getElementById('date-picker');
        console.log('Date picker element:', datePickerElement);

        if (datePickerElement && typeof flatpickr === 'function') {
            console.log('Initializing flatpickr...');

            const datePicker = flatpickr("#date-picker", {
                enableTime: true,
                dateFormat: "F j, Y at h:i K",
                minDate: "today",
                maxDate: new Date().fp_incr(30),
                inline: true,
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
                onChange: function(selectedDates, dateStr) {
                    console.log('Selected datetime:', dateStr);
                    const checkButton = document.getElementById('check-availability-button');
                    if (checkButton) {
                        checkButton.style.display = 'block';
                    }
                }
            });

            console.log('Flatpickr initialized:', datePicker);

            // Handle availability check
            const checkButton = document.getElementById('check-availability-button');
            if (checkButton) {
                checkButton.addEventListener('click', function() {
                    const selectedDate = datePicker.selectedDates[0];
                    console.log('Selected date object:', selectedDate);

                    if (selectedDate) {
                        const dateParam = selectedDate.toISOString().split('T')[0];
                        const timeParam = selectedDate.toTimeString().slice(0, 5);
                        console.log('Date param:', dateParam);
                        console.log('Time param:', timeParam);

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
    }, 100); // Small delay to ensure everything is loaded
});