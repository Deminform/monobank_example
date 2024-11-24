
import json
import certifi
import ssl
import aiohttp
import asyncio
from fastapi import status
from dotenv import dotenv_values

config = dotenv_values(".env")

ssl_context = ssl.create_default_context(cafile=certifi.where())
CREATE_INVOICE_PATH = 'https://api.monobank.ua/api/merchant/invoice/create'
HEADERS = {
        'Content-Type': 'application/json',
        'X-Token': config.get("MONO_TOKEN")
    }

async def create_invoice_mono(product: dict) -> dict:
    """Функція для стровення інвойсу"""
    print("Start create_invoice")
    body = {
        "amount": int(product["amount"] * 100), 
        "ccy": 980,
        "merchantPaymInfo": {
            "reference": str(product["reference"]),
            "destination": product["destination"]},
        "redirectUrl": f"https://casual-fresh-burro.ngrok-free.app/success",
        "webHookUrl":  "https://casual-fresh-burro.ngrok-free.app/payment/monopay",
        "validity": 3600,
        "paymentType": "debit"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url=CREATE_INVOICE_PATH, headers=HEADERS, data=json.dumps(body),
                                ssl=ssl_context) as response:
            if response.status == status.HTTP_200_OK:
                print(f"{response.status=}")
                result = await response.json()
                return result
            print(f"{response.status=}")
            result = await response.json()
            print(result)
            
if __name__ == "__main__":
    product = {"amount": 10, "reference": "14", "destination": "Оплата за курси Python"}
    print(asyncio.run(create_invoice_mono(product)))