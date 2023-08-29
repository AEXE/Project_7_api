FROM python:3.11-slim

WORKDIR /app

COPY . /app
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get -y install curl
RUN apt-get install libgomp1
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=127.0.0.1
ENV FLASK_ENV=production

EXPOSE 8080
EXPOSE 80

CMD ["gunicorn", "app:app", "-b", "0.0.0.0:8080", "--workers", "3"]

