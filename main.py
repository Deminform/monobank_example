import uvicorn
import json
import certifi
import ssl
from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware
import aiohttp
from typing import Any
from fastapi import FastAPI, status
from dotenv import dotenv_values

config = dotenv_values(".env")
print(config)
ssl_context = ssl.create_default_context(cafile=certifi.where())

webHookUrl = "https://casual-fresh-burro.ngrok-free.app/payment/monopay"

async def subscribe_to_mono(webhook_url: str):
    print('Run subscribe to mono')
    mono_url = 'https://api.monobank.ua/personal/webhook'
    body = {
        "webHookUrl": webHookUrl,
    }
    headers = {
        'Content-Type': 'application/json',
        'X-Token': config.get("MONO_TOKEN")
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(mono_url, data=json.dumps(body), headers=headers, ssl=ssl_context) as resp:
            print(resp.status)
            if resp.status == 200:
                return await resp.json()
            else:
                print(resp.text)


@asynccontextmanager
async def lifespan(fastapi_app: FastAPI):
    await subscribe_to_mono(webhook_url=webHookUrl)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/success")
async def root():
    return {"message": "Дякуємо за покупку"}


@app.get("/payment/monopay", status_code=status.HTTP_200_OK)
async def get_monopay():
    print('Start get')
    return {"message": status.HTTP_200_OK}


@app.post("/payment/monopay", status_code=status.HTTP_200_OK)
async def post_monopay(data: Any|dict):
    print(f'Start post: {data}')
    return {"message": status.HTTP_200_OK}





if __name__ == '__main__':
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)
