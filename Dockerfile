FROM python:latest

WORKDIR . /app

COPY requirements.txt .

RUN python3 -m pip install -r requirements.txt

COPY . /app

CMD ["python3", "/app/cityweather.py"]
