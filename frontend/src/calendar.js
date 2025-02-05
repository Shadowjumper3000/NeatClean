document.getElementById('check-availability-button').addEventListener('click', function() {
    const date = document.getElementById('date-picker').value;
    const time = document.getElementById('time-picker').value;
    if (date && time) {
        const url = new URL("/staff-list/", window.location.origin);
        url.searchParams.append('date', date);
        url.searchParams.append('time', time);
        window.location.href = url.toString();
    } else {
        alert('Please select both date and time.');
    }
});

document.getElementById('date-picker').addEventListener('change', function() {
    const datePicker = document.getElementById('date-picker');
    const timeContainer = document.getElementById('time-container');
    if (datePicker.value) {
        timeContainer.style.display = 'block';
    } else {
        timeContainer.style.display = 'none';
    }
});