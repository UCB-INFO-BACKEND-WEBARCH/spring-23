from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from worker import sendEmailTask

app = Flask(__name__, template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@db:5432/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Registration(db.Model):
    email = db.Column(db.String(120), primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Registration %r>' % self.email


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/register', methods=["POST"])
def register():
    email = request.get_json()['email']
    name = request.get_json()['name']
    new_registration = Registration(email=email, name=name)
    db.session.add(new_registration)
    db.session.commit()
    return 'Registration successful!'


@app.route('/send', methods=["POST"])
def sendEmails():
    data = request.get_json()
    emailBody = data['body']
    emailSubject = data['subject']

    registrations = Registration.query.all()
    emails = [registration.email for registration in registrations]
    taskIDs = []
    for email in emails:
        emailAsyncTask = sendEmailTask.delay(email, emailBody, emailSubject)
        taskIDs.append(emailAsyncTask.id)
    return {"tasks": taskIDs}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
