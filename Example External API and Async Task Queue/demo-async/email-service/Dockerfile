FROM python:3.9-alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["-m", "flask", "--app", "send_email_server", "run", "--host=0.0.0.0", "--port=5000"]