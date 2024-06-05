FROM python:3.10-alpine

WORKDIR /app
COPY . /app

RUN pip3 install pipenv && pipenv install

CMD [ "pipenv", "run", "python", "app.py" ]
