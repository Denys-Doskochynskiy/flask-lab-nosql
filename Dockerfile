FROM python:3.8
COPY ./requirements.txt /app/requirements.txt
COPY ./.env /app/.env

WORKDIR /app
RUN apt-get update && apt-get install -y git vim python3-pip python3-venv

RUN pip3 install -r requirements.txt
COPY . /app
EXPOSE 5000
ENTRYPOINT [ "python3" ]
CMD ["app.py" ]