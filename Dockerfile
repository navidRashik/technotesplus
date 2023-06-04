FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1
ENV DEBIAN_FRONTEND noninteractive

# Creating working directory
RUN mkdir /app
WORKDIR /app

# Set timezone
RUN echo "Asia/Dhaka" > /etc/timezone

# Install project dependencies
COPY ./requirements.txt ./


RUN apt-get update \
    && apt-get install build-essential tzdata -y \
    && python3 -m pip install --upgrade pip -r requirements.txt gunicorn uvicorn\
    && apt-get remove build-essential -y \
    && apt-get autoremove -y 

# Copy project files
COPY . .

CMD python manage.py migrate; python manage.py collectstatic --noinput; gunicorn ihost.asgi:application -w 3 -k uvicorn.workers.UvicornH11Worker -b [::]:$PORT
