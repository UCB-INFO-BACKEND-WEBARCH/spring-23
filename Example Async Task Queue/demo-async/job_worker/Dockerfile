FROM python:3.9-alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ADD https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/tokenizers/punkt.zip /tmp/nltk/
RUN mkdir -p /nltk_data/tokenizers/
RUN unzip /tmp/nltk/punkt.zip -d /nltk_data/tokenizers/
ENTRYPOINT ["celery"]
CMD ["-A", "job_tasks.celery_app", "worker"]