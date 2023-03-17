FROM python:3.9-alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["celery"]
CMD ["-A", "worker.celery_app", "worker"]