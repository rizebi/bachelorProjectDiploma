FROM ubuntu:16.04

RUN apt-get update -y
RUN apt-get install -y python-pip python-dev
# COPY ./requirements.txt /app/requirements.txt
RUN pip install mysql-connector-python-rf
WORKDIR /app
EXPOSE 5000
# RUN pip install -r requirements.txt
COPY . /app
ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
