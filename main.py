from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator
import requests
import re
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Logger configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

app = FastAPI()

# Constants
API_VERSION = os.getenv("WHATSAPP_API_VERSION", "v17.0")
PHONE_NUMBER_ID = os.getenv("WHATSAPP_PHONE_NUMBER_ID")
ACCESS_TOKEN = os.getenv("WHATSAPP_ACCESS_TOKEN")

if not PHONE_NUMBER_ID or not ACCESS_TOKEN:
    raise RuntimeError("Missing required environment variables.")

WHATSAPP_API_URL = f"https://graph.facebook.com/{API_VERSION}/{PHONE_NUMBER_ID}/messages"

# Request model
class PhoneNumberModel(BaseModel):
    phone_number: str

    @validator("phone_number")
    def validate_phone_number(cls, v):
        v = '+' + v.strip().lstrip('+')
        if not re.match(r"^\+\d{10,15}$", v):
            raise ValueError("Invalid phone number format. Use E.164 format (e.g., +12345678900).")
        return v

# Error parsing
def parse_whatsapp_error(response_json):
    error = response_json.get("error", {})
    code = error.get("code")
    message = error.get("message", "An unknown error occurred.")
    logger.error(f"Error Code: {code}, Message: {message}")

    # Return appropriate message and HTTP status
    if code == 131030:
        return (
            400,
            {
                "error": "Phone number not allowed",
                "message": "The recipient's phone number is not in the WhatsApp allowed list. Add it and try again."
            }
        )
    else:
        return (
            500,
            {
                "error": "WhatsApp API error",
                "message": message
            }
        )

# Endpoint
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
                "name": "tmbc",
                "language": {"code": "en"}
            }
        }

        response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
        logger.info(f"Status Code: {response.status_code}")
        logger.info(f"Response JSON: {response.json()}")

        if response.status_code != 200:
            status_code, error_detail = parse_whatsapp_error(response.json())
            raise HTTPException(status_code=status_code, detail=error_detail)

        return {
            "status": "Message sent successfully",
            "whatsapp_response": response.json()
        }

    except ValueError as ve:
        logger.error(f"Validation Error: {ve}")
        raise HTTPException(status_code=400, detail={"error": "Validation error", "message": str(ve)})
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.exception("Unexpected server error")
        raise HTTPException(status_code=500, detail={"error": "Server error", "message": "Something went wrong."})
