# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

# Install dependencies
COPY requirements.txt /code/

RUN pip install -r requirements.txt

RUN python manage.py collectstatic --noinput
# Copy project
COPY . /code/
