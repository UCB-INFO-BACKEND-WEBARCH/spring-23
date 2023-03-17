import os
from celery import Celery
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

broker_url = os.environ.get("CELERY_BROKER_URL"),
res_backend = os.environ.get("CELERY_RESULT_BACKEND")

celery_app = Celery(name='worker',
                    broker=broker_url,
                    result_backend=res_backend)


@celery_app.task
def sendEmailTask(email, emailBody, emailSubject):
    try:
        message = Mail(
            from_email=os.environ.get('SENDGRID_FROM_EMAIL'),
            to_emails=email,
            subject=emailSubject,
            html_content=emailBody
        )
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        return response
    except Exception as e:
        print(e)
        return str(e)