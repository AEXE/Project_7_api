FROM python:3.11-slim

WORKDIR /app

COPY . /app
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get -y install curl
RUN apt-get install libgomp1
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


EXPOSE 5000

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

