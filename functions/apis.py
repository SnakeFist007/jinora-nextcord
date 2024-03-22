import os
import aiohttp
import requests
from dotenv import load_dotenv
from functions.logging import logging

load_dotenv()
QUOTES = os.getenv("QUOTES")
WEATHER = os.getenv("WEATHER")


# * API scheme from https://api-ninjas.com
async def apininjas(url: str) -> dict:
    res = requests.get(url, headers={"X-Api-Key": QUOTES})
    data = res.json()

    if res.status_code == requests.codes.ok:
        return data
    else:
        logging.exception("ERROR getting response from quotes API")
        raise ValueError



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