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
    low_amt = request.args.get('low_amt', "0")
    high_amt = request.args.get('high_amt', "0")

    start_sql = datetime.date(int(start.split("/")[1]), int(start.split("/")[0]), 1)
    end_sql = datetime.date(int(end.split("/")[1]), int(end.split("/")[0]), 1)
    states_sql = tuple(states.split(","))
    types_sql = tuple(types.split(","))
    low_amt_sql = int(low_amt)
    high_amt_sql = int(high_amt)


    stmt_sql = """ SELECT state, type, amount, date
                    FROM energy_consumption
                    WHERE date BETWEEN :start_sql AND :end_sql
                    AND state IN :states_sql
                    AND type IN :types_sql
    """

    if low_amt_sql != 0 or high_amt_sql != 0:
        stmt_sql += "AND amount BETWEEN :low_amt_sql AND :high_amt_sql"

    stmt = text(stmt_sql)

    if low_amt_sql != 0 or high_amt_sql != 0:
        stmt = stmt.bindparams(start_sql=start_sql, 
                            end_sql=end_sql,
                            states_sql=states_sql,
                            types_sql=types_sql,
                            low_amt_sql=low_amt_sql,
                            high_amt_sql=high_amt_sql)
    else:
        stmt = stmt.bindparams(start_sql=start_sql, 
                            end_sql=end_sql,
                            states_sql=states_sql,
                            types_sql=types_sql)

    result = db.session.execute(stmt).all()

    result_json = {}
    result_rows = []

    for row in result:
        current_row_data = {"state": row[0], "type": row[1], "amount": row[2], "date": row[3].strftime("%m/%y")}
        result_rows.append(current_row_data)

    result_json["results"] = result_rows
    return json.dumps(result_json)