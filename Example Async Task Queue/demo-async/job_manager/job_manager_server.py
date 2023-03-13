from flask import Flask, request
from job_tasks import count_words_from_url, celery_app
from celery.result import AsyncResult
import json

app = Flask(__name__)

@app.route('/submit_count_words_url_job', methods = ['POST'])
def count_words_url():
    data = request.get_json()
    url = data.get("url")

    result = count_words_from_url.delay(url)
    return json.dumps({"id": result.id})

@app.route('/get_result_count_words_url_job/<id>', methods = ['GET'])
def get_count_words_url(id):

    res = AsyncResult(id, app=celery_app)
    count = -1
    if res.status == "SUCCESS":
        count = res.get()

    return json.dumps({"count": count})
    
    

