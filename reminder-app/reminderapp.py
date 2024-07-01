import schedule
import time
from plyer import notification
from datetime import datetime, timedelta

def send_reminder(reminder_name):
    notification.notify(
        title="Reminder",
        message=f"Remember to: {reminder_name}",
        timeout=10  # Notification duration in seconds
    )

def setup_reminder(reminder_name, start_date, end_date, reminder_time):
    # Schedule the reminder to run daily at the specified time
    schedule.every().day.at(reminder_time).do(send_reminder, reminder_name=reminder_name)

    while datetime.now().date() <= end_date:
        schedule.run_pending()
        time.sleep(2)  # Sleep for a minute before checking again

if __name__ == "__main__":
    reminder_name = "Water the plant"
    start_date = datetime.strptime("2024-04-24", '%Y-%m-%d').date()
    end_date = datetime.strptime("2024-04-30", '%Y-%m-%d').date()
    reminder_time = "21:11"  # 24-hour format

    setup_reminder(reminder_name, start_date, end_date, reminder_time)
