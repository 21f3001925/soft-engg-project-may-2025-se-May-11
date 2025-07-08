from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

# from message import send_sms


def send_medication_reminder():
    print(
        f"[{datetime.now()}] Medication reminder triggered!"
    )  # Replace with actual logic


def start_scheduler():
    scheduler = BackgroundScheduler()
    # Schedule the job (e.g., every day at 9 AM)
    scheduler.add_job(send_medication_reminder, "cron", hour=14, minute=38)
    scheduler.start()
    # send_sms("+916351838115", "Take your Medicine")
    # send_sms("+919884659616", "Take your Medicine")
    # send_sms("+919347714177", "Take your Medicine")
    # send_sms("+919496709986", "Take your Medicine")
    print("Scheduler started.")
