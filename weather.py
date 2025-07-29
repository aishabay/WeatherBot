from http import HTTPStatus

import aiohttp

from config import WEATHER_API_KEY


async def get_weather(city: str) -> str:
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": WEATHER_API_KEY,
        "units": "metric",
        "lang": "ru",
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status != HTTPStatus.OK:
                return "Город не найден!"

            data = await response.json()

    temp = data["main"]["temp"]
    description = data["weather"][0]["description"]
    return f"{temp}°C в {city}: {description}"
