from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import json

app = Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@db:5432/quote-db"
db.init_app(app)

def gen_response(day_of_week):
    if not day_of_week:
        response = {"message": "We need the day_of_week in order to send a quote"}
        response_code = 400
    else:
        stmt = text("SELECT quote FROM quotes WHERE day_of_week = :x")
        stmt = stmt.bindparams(x=day_of_week)
        result = db.session.execute(stmt).all()

        if not result:
             response = {"message": "Sorry we don't know that day of the week" }
             response_code = 404
        else:
            response = {"day": day_of_week, "quote": result[0].quote}
            response_code = 200

    return json.dumps(response), response_code

@app.route('/quote/<day_of_week>')
def quote_of_the_day(day_of_week):
    return gen_response(day_of_week)

@app.route('/quote', methods = ['GET'])
@app.route('/quote/', methods = ['GET'])
def quote_of_the_day_get():
    day_of_week = request.args.get("day_of_week")
    return gen_response(day_of_week)

@app.route('/quote', methods = ['POST'])
def quote_of_the_day_post():
    data = request.get_json()
    day_of_week = data.get("day_of_week")
    return gen_response(day_of_week)
