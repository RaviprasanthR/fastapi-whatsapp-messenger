from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
import requests
import re
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file (if present)
load_dotenv()

# Configure logger
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Constants
API_VERSION = os.getenv("WHATSAPP_API_VERSION", "v17.0")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")

if not PHONE_NUMBER_ID:
    raise RuntimeError("Phone number ID is missing from environment variables.")

WHATSAPP_API_URL = f"https://graph.facebook.com/{API_VERSION}/{PHONE_NUMBER_ID}/messages"

ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")

if not ACCESS_TOKEN:
    raise RuntimeError("WhatsApp Access Token is missing in environment variables.")

class PhoneNumberModel(BaseModel):
    phone_number: str

    @validator("phone_number")
    def validate_phone_number(cls, v):
        v = '+' + v.strip().lstrip('+')
        pattern = re.compile(r"^\+\d{10,15}$")
        if not pattern.match(v):
            raise ValueError("Invalid phone number format. Use E.164 format (e.g., +12345678900).")
        return v

@app.post("/send_message")
def send_message(data: PhoneNumberModel):
    try:
        headers = {
            "Authorization": f"Bearer {ACCESS_TOKEN}",
            "Content-Type": "application/json"
        }

        payload = {
            "messaging_product": "whatsapp",
            "to": data.phone_number,
            "type": "template",
            "template": {
                "name": "hello_world",
                "language": {"code": "en_us"}
            }
        }

        response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
        logger.info(f"Status Code: {response.status_code}")
        logger.info(f"Response JSON: {response.json()}")

        if response.status_code != 200:
            error_data = response.json().get('error', {})
            error_code = error_data.get('code', None)
            error_message = error_data.get('message', '')

            if error_code == 131030:
                error_detail = "The recipient's phone number is not registered on WhatsApp or is not part of the allowed list. Please verify the phone number and try again."
                raise HTTPException(status_code=400, detail=error_detail)

            # Handle other specific error codes as needed
            raise HTTPException(status_code=500, detail=f"Error from WhatsApp API: {error_message}")

        return {
            "status": "Message sent successfully",
            "whatsapp_response": response.json()
        }

    except ValueError as ve:
        logger.error(f"Validation Error: {ve}")
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        logger.exception("An unexpected error occurred.")
        raise HTTPException(status_code=500, detail="An unexpected error occurred.")
