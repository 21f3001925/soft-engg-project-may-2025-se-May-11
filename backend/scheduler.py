from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime


def send_medication_reminder():
    print(
        f"[{datetime.now()}] Medication reminder triggered!"
    )  # Replace with actual logic


def start_scheduler():
    scheduler = BackgroundScheduler()
    # Schedule the job (e.g., every day at 9 AM)
    scheduler.add_job(send_medication_reminder, "cron", hour=19, minute=16)
    scheduler.start()
    print("Scheduler started.")
