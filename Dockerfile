FROM python:3.11-slim

WORKDIR /app

RUN python -m pip install 'poetry==1.6.1'

COPY pyproject.toml poetry.lock  /app/

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY resources /app/resources
COPY cityweather.py /app

CMD ["uvicorn", "app:cityweather", "--host", "0.0.0.0", "--port", "8080"]
