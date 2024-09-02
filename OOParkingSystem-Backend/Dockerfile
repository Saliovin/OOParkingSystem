FROM python:3.10-alpine

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN apk add postgresql-dev

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code

ENTRYPOINT ["./scripts/daemon.sh"]