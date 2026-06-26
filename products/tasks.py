import time
from celery import shared_task


@shared_task
def send_welcome_email_task(user_email):
    print(f"--- Starting to send welcome email to {user_email} ---")
    
    time.sleep(5)
    
    print(f"--- Email successfully sent to {user_email} ---")
    return f"Email sent to {user_email}"