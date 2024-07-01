import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
import schedule
import time
from plyer import notification
from threading import Thread
import json
import os

# File to store reminders
REMINDER_FILE = 'reminders.json'

def send_reminder(reminder_name):
    notification.notify(
        title='Reminder',
        message=f'{reminder_name}',
        #app_icon=None,  # Path to app icon image file if desired
        timeout=10  # Notification duration in seconds
    )

def save_reminders(data):
    with open(REMINDER_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def load_reminders():
    if os.path.exists(REMINDER_FILE):
        with open(REMINDER_FILE, 'r') as f:
            return json.load(f)
    return []

def start_reminder():
    reminder_name = reminder_text.get().strip()
    reminder_time = time_combo.get().strip()
    start_date = start_date_entry.get().strip()
    end_date = end_date_entry.get().strip()

    if reminder_name and reminder_time and start_date and end_date:
        try:
            time.strptime(reminder_time, '%H:%M')
        except ValueError:
            print("Invalid time format. Please enter time as HH:MM")
            return

        reminder_data = {
            'reminder_name': reminder_name,
            'reminder_time': reminder_time,
            'start_date': start_date,
            'end_date': end_date
        }

        reminders = load_reminders()
        reminders.append(reminder_data)
        save_reminders(reminders)  # Save reminder settings
        update_reminder_listbox(reminders)  # Update GUI listbox

        schedule.clear()  # Clear existing jobs
        for reminder in reminders:
            schedule.every().day.at(reminder['reminder_time']).do(send_reminder, reminder_name=reminder['reminder_name'])

        def run_scheduler():
            while True:
                schedule.run_pending()
                time.sleep(60)  # Sleep for a minute

        thread = Thread(target=run_scheduler)
        thread.daemon = True
        thread.start()

def update_reminder_listbox(reminders):
    reminder_listbox.delete(0, tk.END)
    for reminder in reminders:
        reminder_listbox.insert(tk.END, f"{reminder['reminder_name']} at {reminder['reminder_time']} from {reminder['start_date']} to {reminder['end_date']}")

def delete_reminder(event):
    # Get the selected item to delete
    selection = reminder_listbox.curselection()
    if not selection:
        return
    index = selection[0]
    reminders = load_reminders()
    reminders.pop(index)  # Remove the reminder from the list
    save_reminders(reminders)  # Save the updated list
    update_reminder_listbox(reminders)  # Update the GUI listbox
    schedule.clear()  # Clear all scheduled jobs
    for reminder in reminders:
        # Re-schedule the remaining reminders
        schedule.every().day.at(reminder['reminder_time']).do(send_reminder, reminder_name=reminder['reminder_name'])

# Add a right-click context menu
def show_context_menu(event):
    try:
        context_menu.tk_popup(event.x_root, event.y_root)
    finally:
        context_menu.grab_release()

# Setup the GUI
root = tk.Tk()
root.title("Reminder Setup")

# Add widgets
ttk.Label(root, text="Reminder Message:").grid(row=0, column=0, padx=10, pady=10)
reminder_text = ttk.Entry(root)
reminder_text.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(root, text="Reminder Time (24h, e.g., 15:00):").grid(row=1, column=0, padx=10, pady=10)
time_combo = ttk.Entry(root)
time_combo.grid(row=1, column=1, padx=10, pady=10)

ttk.Label(root, text="Start Date:").grid(row=2, column=0, padx=10, pady=10)
# Use the DateEntry widget instead of a simple Entry
start_date_entry = DateEntry(root, date_pattern='y-mm-dd')
start_date_entry.grid(row=2, column=1, padx=10, pady=10)

ttk.Label(root, text="End Date:").grid(row=3, column=0, padx=10, pady=10)
# Use the DateEntry widget instead of a simple Entry
end_date_entry = DateEntry(root, date_pattern='y-mm-dd')
end_date_entry.grid(row=3, column=1, padx=10, pady=10)

ttk.Button(root, text="Set Reminder", command=start_reminder).grid(row=4, column=1, padx=10, pady=10)

reminder_listbox = tk.Listbox(root, width=50, height=10)
reminder_listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

# Create a context menu
context_menu = tk.Menu(root, tearoff=0)
context_menu.add_command(label="Delete", command=lambda: delete_reminder(None))

# Bind right-click to the context menu
reminder_listbox.bind("<Button-3>", show_context_menu)
reminder_listbox.bind("<Button-2>", show_context_menu)  # For macOS compatibility

# Load reminders on start and schedule them
def initial_load():
    reminders = load_reminders()
    update_reminder_listbox(reminders)
    for reminder in reminders:
        reminder_text.delete(0, tk.END)
        time_combo.delete(0, tk.END)
        start_date_entry.delete(0, tk.END)
        end_date_entry.delete(0, tk.END)

        reminder_text.insert(0, reminder['reminder_name'])
        time_combo.insert(0, reminder['reminder_time'])
        start_date_entry.insert(0, reminder['start_date'])
        end_date_entry.insert(0, reminder['end_date'])
        
        start_reminder()  # This is now safe due to the check within the function

root.after(100, initial_load)

# Start the GUI event loop
root.mainloop()
