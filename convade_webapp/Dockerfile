# base python image
FROM python:3.10-slim

# avoid .pyc files and enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# install system packages needed to build some Python packages (psycopg2)
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# copy and install python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# copy project code
COPY . /app/

EXPOSE 8000

# use Django runserver for dev so you can see hot changes via volume mount
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
