import os
import aiohttp
import requests
from dotenv import load_dotenv
from functions.logging import logging

load_dotenv()
API_QUOTES = os.getenv("QUOTES")
API_WEATHER = os.getenv("WEATHER")


class Session:
    def __init__(self, url, headers):
        self.url = url
        self.headers = headers

    def __enter__(self):
        self.session = requests.Session()
        self.response = self.session.get(self.url, headers=self.headers)
        return self.response
    
    def __exit__(self):
        self.session.close()


# * API scheme from https://api-ninjas.com
async def apininjas(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        headers = { "X-Api-Key": API_QUOTES }
        
        async with session.get(url, headers=headers) as res:
            data = await res.json()
            
        if res.status == 200:
            return data
        else:
            logging.exception("ERROR getting response from quotes API: %s", data)
            raise ValueError("Failed to fetch data from quotes API")


# * API scheme from https://weatherapi.com
async def weatherapi(url: str, location: str) -> dict:
    async with aiohttp.ClientSession() as session:
        params = { "key": API_WEATHER, "q": location }
        
        async with session.get(url, params=params) as res:
            data = await res.json()
            
        if res.status == 200:
            return data
        else:
            logging.exception("ERROR getting response from weather API: %s", data)
            raise ValueError("Failed to fetch data from weather API")
    
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