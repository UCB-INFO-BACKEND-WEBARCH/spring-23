from flask import Flask, request
import json
import logging
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)

@app.route('/email', methods = ['POST'])
def quote_of_the_day_post():

    if request.headers.get("Content-Type") == 'application/json':

        data = request.get_json()
        to_email = data.get("to")
        from_email = data.get("from")
        subject = data.get("subject")
        body = data.get("body")

        if not to_email or not from_email or not subject or not body:
            response = {"message": "Please fill out all fields to send an email"}
            response_code = 400           
        else:
            message = Mail(
                from_email=from_email,
                to_emails=to_email,
                subject=subject,
                html_content=body)
            try:
                sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
                sg.send(message)
                response = {"message": "Email was sent"}
                response_code = 200
            except Exception as e:
                logging.error(e)
    else:
        response = {"message": "Endpoint requires json input"}
        response_code = 400 
    
    return json.dumps(response), response_code
        