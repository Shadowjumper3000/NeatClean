function bookCleaner(staffId, staffName) {
  const address = prompt("Please enter your address:");
  const date = document.getElementById('date').value;
  const time = document.getElementById('time').value;
  const dateTime = `${date} ${time}`;

  const bookingData = { staffId, staffName, address, dateTime };

  console.log('Booking Data:', bookingData);

  // Save booking to Google Sheets
  fetch('https://script.google.com/macros/s/AKfycbyvHsXdrzkRU5C9Zguw21akJYmTyJN8BkY-78IAZe_o6O3crELmNmHmOJ2Os078b4j8/exec', { // Replace with your Apps Script URL
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(bookingData)
  })
  .then(response => response.json())
  .then(data => {
    console.log('Response Data:', data);
    if (data.success) {
    alert("Booking saved! You can check the status on the home page.");
    window.location.href = "index.html"; // Redirect to home page
    } else {
    alert("Failed to save booking. Try again.");
    }
  })
  .catch(error => {
    console.error('Error:', error);
    alert("An error occurred. Please try again.");
    });
}
