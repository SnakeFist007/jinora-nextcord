import os
import aiohttp
import requests
from dotenv import load_dotenv
from functions.logging import logging
from functions.helpers import JSONLoader, daily_random
from functions.paths import questions, en_mood_comments, de_mood_comments

load_dotenv()
WEATHER = os.getenv("WEATHER")
QUOTES = os.getenv("QUOTES")


# * API scheme from https://api-ninjas.com
async def apininjas(url: str) -> dict:
    res = requests.get(url, headers={"X-Api-Key": QUOTES})
    data = res.json()

    if res.status_code == requests.codes.ok:
        return data
    else:
        logging.exception("ERROR getting response from quotes API")
        raise ValueError

# Functions used with api-ninjas
async def get_quote(lang) -> dict:
    if lang == "en":
        url = "https://api.api-ninjas.com/v1/quotes?category=inspirational"
        return await apininjas(url)
    elif lang == "de":
        url = "https://api.api-ninjas.com/v1/quotes?category=inspirational"
        return await apininjas(url)



# * API scheme from https://weatherapi.com
async def weatherapi(url: str, location: str) -> dict:
    params = {
        "key": WEATHER,
        "q": location
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as res:
            data = await res.json()

    return data
    
# Functions used with weatherapi


async def get_weather(location: str) -> dict:
    try:
        url = "https://api.weatherapi.com/v1/current.json"   
        return await weatherapi(url, location)
    
    except KeyError as e:
        logging.exception(e)
        raise e
    

async def get_astro(location: str) -> dict:
    try:
        url = "https://api.weatherapi.com/v1/astronomy.json"
        return await weatherapi(url, location)
    
    except KeyError as e:
        logging.exception(e)
        raise e
    
    
# * Random question grabber
def get_question(lang: str) -> str:
    if lang == "en":
        lines = JSONLoader.load(questions)
    elif lang == "de":
        lines = JSONLoader.load(questions)
    
    length = len(lines)
    rand_int = daily_random(length)
    
    return lines[str(rand_int)]


# * Random comment grabber
def get_mood(lang: str) -> str:
    if lang == "en":
        input = en_mood_comments
    elif lang == "de":
        input = de_mood_comments
    
    lines = JSONLoader.load(input)
    length = len(lines)
    rand_int = daily_random(length)

    return lines[str(rand_int)]