// static/dashboard.js
document.addEventListener('DOMContentLoaded', function() {
  const medicationForm = document.getElementById('medication-form');
  const remindersList = document.getElementById('reminders-list');
  
  // Load existing reminders from localStorage
  let reminders = JSON.parse(localStorage.getItem('reminders')) || [];
  updateRemindersList();
  
  medicationForm.addEventListener('submit', function(e) {
      e.preventDefault();
      
      const medName = document.getElementById('med-name').value;
      const medTime = document.getElementById('med-time').value;
      
      if (medName && medTime) {
          reminders.push({ name: medName, time: medTime });
          localStorage.setItem('reminders', JSON.stringify(reminders));
          updateRemindersList();
          setupReminders();
          
          // Clear form
          medicationForm.reset();
      }
  });
  
  function updateRemindersList() {
      remindersList.innerHTML = '';
      reminders.forEach((reminder, index) => {
          const reminderElement = document.createElement('div');
          reminderElement.className = 'reminder-item';
          reminderElement.innerHTML = `
              <span>${reminder.name} - ${reminder.time}</span>
              <button onclick="deleteReminder(${index})">Delete</button>
          `;
          remindersList.appendChild(reminderElement);
      });
  }
  
  function setupReminders() {
      // Clear existing notifications
      if ('Notification' in window) {
          Notification.requestPermission().then(function(permission) {
              if (permission === 'granted') {
                  reminders.forEach(reminder => {
                      const [hours, minutes] = reminder.time.split(':');
                      
                      // Schedule notification
                      setInterval(() => {
                          const now = new Date();
                          if (now.getHours() === parseInt(hours) && 
                              now.getMinutes() === parseInt(minutes)) {
                              new Notification('Medication Reminder', {
                                  body: `Time to take ${reminder.name}!`,
                              });
                          }
                      }, 60000); // Check every minute
                  });
              }
          });
      }
  }
  
  // Expose deleteReminder to global scope
  window.deleteReminder = function(index) {
      reminders.splice(index, 1);
      localStorage.setItem('reminders', JSON.stringify(reminders));
      updateRemindersList();
  };
  
  // Initial setup of reminders
  setupReminders();
});