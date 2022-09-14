from .celery import app
from account.send_email import send_confirmation_email, send_notification

@app.task 
def send_email_task(to_email,code):
    send_confirmation_email(to_email,code)


@app.task
def send_beat_email(email,id):
    send_notification(email,id)
