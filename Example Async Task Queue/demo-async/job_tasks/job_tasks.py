import os
from celery import Celery
import requests
from collections import Counter
from bs4 import BeautifulSoup
import re
import nltk

broker_url  = os.environ.get("CELERY_BROKER_URL"),
res_backend = os.environ.get("CELERY_RESULT_BACKEND")

celery_app = Celery(name           = 'job_tasks',
                    broker         = broker_url,
                    result_backend = res_backend)

@celery_app.task
def count_words_from_url(url):
    try:
        r = requests.get(url)
    except:
        return 0

    if r:
        # text processing
        raw = BeautifulSoup(r.text, 'html.parser').get_text()
        tokens = nltk.word_tokenize(raw)
        text = nltk.Text(tokens)
        # remove punctuation, count raw words
        nonPunct = re.compile('.*[A-Za-z].*')
        raw_words_count = len([w for w in text if nonPunct.match(w)])
        return raw_words_count
    
    return 0
        
        