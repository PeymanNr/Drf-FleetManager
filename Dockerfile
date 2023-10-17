FROM python:3.10

LABEL maintainer="Peyman Naseri <ipeymann@gmail.com>"

RUN mkdir /fleetmanager
WORKDIR /fleetmanager

RUN apt update
RUN apt install -y python3-pip

COPY requirements.txt /fleetmanager
RUN pip install -r requirements.txt

COPY . /fleetmanager

EXPOSE 5000

# Define the command to run when the container starts
CMD python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8888
