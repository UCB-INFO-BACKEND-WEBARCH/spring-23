from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import json
import os
import datetime

app = Flask(__name__)
db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
db.init_app(app)

@app.route('/filtered_data/', methods=["GET"])
def filtered_data():
    start = request.args.get("start")
    end = request.args.get("end")
    states = request.args.get("states")
    types = request.args.get("types")
    low_amt = request.args.get('low_amt', 0)
    high_amt = request.args.get('high_amt', 0)

    start_sql = datetime.date(start.split("/")[1], start.split("/")[0], 1)
    end_sql = datetime.date(end.split("/")[1], end.split("/")[0], 1)
    states_sql = states.split(",")
    types_sql = types.split(",")
    low_amt_sql = low_amt
    high_amt_sql = high_amt


    stmt_sql = """ SELECT state, type, amount, date
                    FROM energy_consumption
                    WHERE date BETWEEN :start_sql AND :end_sql
                    AND state IN :states_sql
                    AND types IN :types_sql
    """

    if low_amt != 0 or high_amt != 0:
        stmt_sql += "AND amount BETWEEN :low_amt_sql AND :high_amt_sql"

    stmt = text(stmt_sql)
    stmt = stmt.bindparams()

    stmt = text("SELECT quote FROM quotes WHERE day_of_week = :x")
        stmt = stmt.bindparams(x=day_of_week)
        result = db.session.execute(stmt).all()



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
