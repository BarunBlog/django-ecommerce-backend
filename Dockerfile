FROM python:3.8

RUN apt update && apt install make

WORKDIR /app

COPY . .

RUN pip3 install -r requirements.txt

CMD [ "make", "runserver"]