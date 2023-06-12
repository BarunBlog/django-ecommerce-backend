FROM python:3.8

RUN apt update && apt install make

WORKDIR /app

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "make", "migrate_and_runserver"]