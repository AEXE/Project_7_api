FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["flask", "run"]
