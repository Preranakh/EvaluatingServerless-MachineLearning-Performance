FROM python:3.8-slim

EXPOSE 5000

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

CMD ["gunicorn", "--workers", "1", "--bind", "0.0.0.0:5000", "app:app"]
