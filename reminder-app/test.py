from plyer import notification

def send_test_notification():
    notification.notify(
        title='Test Notification',
        message='This is a test notification to check functionality.',
        #app_icon=None,  # Optional: specify a path to an .ico file for the notification icon
        timeout=10  # Notification display duration in seconds
    )

if __name__ == "__main__":
    send_test_notification()
