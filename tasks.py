from celery import Celery

app = Celery('tasks', broker='django://')


@app.task
def send_mail(mail):
    mail.send()
