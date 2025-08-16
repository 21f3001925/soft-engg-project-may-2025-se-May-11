/**
 * Returns a string like "1 month 2 weeks left" or "Overdue"
 * @param {string|Date} dateTimeStr - Appointment time as ISO string or Date
 * @param {Date} [now=new Date()] - Current time, defaults to now
 * @returns {string}
 */
export function getReminderTime(dateTimeStr, now = new Date()) {
  const appointmentTime = new Date(dateTimeStr);
  const diffMs = appointmentTime - now;

  if (diffMs <= 0) {
    return 'Overdue';
  }

  const diffMinutes = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMinutes / 60);
  const minutes = diffMinutes % 60;

  let months = 0;
  let weeks = 0;
  let days = 0;
  let hours = 0;

  if (diffHours >= 24) {
    days = Math.floor(diffHours / 24);
    hours = diffHours % 24;
  } else {
    hours = diffHours;
  }

  if (days >= 7) {
    weeks = Math.floor(days / 7);
    days = days % 7;
  }

  if (weeks >= 4) {
    months = Math.floor(weeks / 4);
    weeks = weeks % 4;
  }

  let timeString = '';
  if (months > 0) timeString += `${months} month${months > 1 ? 's' : ''} `;
  if (weeks > 0) timeString += `${weeks} week${weeks > 1 ? 's' : ''} `;
  if (days > 0) timeString += `${days} day${days > 1 ? 's' : ''} `;
  if (hours > 0) timeString += `${hours} hour${hours > 1 ? 's' : ''} `;
  if (minutes > 0) timeString += `${minutes} minute${minutes > 1 ? 's' : ''} `;

  return timeString.trim() + ' left';
}
