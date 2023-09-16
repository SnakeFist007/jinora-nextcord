import aiohttp
import requests
from functions.logging import logging
from main import WEATHER, QUOTES

async def apininjas(url):
    res = requests.get(url, headers={"X-Api-Key": QUOTES})
    data = res.json()

    if res.status_code == requests.codes.ok:
        return data
    else:
        logging.exception("ERROR getting response from quotes API")
        raise ValueError


async def get_quote():
    url = "https://api.api-ninjas.com/v1/quotes?category=inspirational"
    return await apininjas(url)



async def weatherapi(url, location):
    params = {
        "key": WEATHER,
        "q": location
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as res:
            data = await res.json()

    return data
    

async def get_weather(location):
    try:
        url = "https://api.weatherapi.com/v1/current.json"   
        return await weatherapi(url, location)
    
    except KeyError as e:
        logging.exception(e)
        raise e
    
async def get_astro(location):
    try:
        url = "https://api.weatherapi.com/v1/astronomy.json"
        return await weatherapi(url, location)
    
    except KeyError as e:
        logging.exception(e)
        raise e
    