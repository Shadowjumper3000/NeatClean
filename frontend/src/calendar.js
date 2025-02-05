document.addEventListener('DOMContentLoaded', function() {
    const datePicker = document.getElementById('date-picker');
    const timeContainer = document.getElementById('time-container');

    datePicker.addEventListener('change', function() {
        if (datePicker.value) {
            timeContainer.style.display = 'block';
        } else {
            timeContainer.style.display = 'none';
        }
    });
});