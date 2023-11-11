from os import environ
from dotenv import load_dotenv
import uvicorn

from cityweather.app import app

load_dotenv()

if __name__ == "__main__":
    host = environ["WEATHER_HOST"]
    port = environ["WEATHER_PORT"]
    log_level = environ["WEATHER_APP_LOG_LEVEL"]

    uvicorn.run(app, host=host, port=int(port), log_level=log_level)
