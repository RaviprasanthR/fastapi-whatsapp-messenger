#Fastapi-Whatsapp-Messenger

This project demonstrates how to create a FastAPI application that integrates with Meta’s WhatsApp Business Manager API to send messages.

## Objective
Create a FastAPI endpoint `/send_message` that sends the following message to a specified WhatsApp number:

```
"Hello, this is a test message from our TMBC bot!"
```

## Features
- Accepts phone number as a query parameter
- Validates phone number format (E.164)
- Integrates with WhatsApp Business API
- Provides error handling and clear responses

## Tech Stack
- Python
- FastAPI
- Pydantic
- Requests

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/whatsapp-fastapi.git
cd whatsapp-fastapi
```

### 2. Create Virtual Environment
```bash
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Replace the placeholders in the main FastAPI file with your actual Meta credentials:
- `YOUR_PHONE_NUMBER_ID`
- `YOUR_ACCESS_TOKEN`

Alternatively, use environment variables and `os.getenv()`.

### 5. Run the Application
```bash
uvicorn main:app --reload
```

## Usage
Visit:
```
http://127.0.0.1:8000/send_message?phone_number=+12345678900
```
Replace `+12345678900` with the actual phone number in E.164 format.

## Example Request
```bash
curl "http://127.0.0.1:8000/send_message?phone_number=+12345678900"
```

## Notes
- Make sure your WhatsApp Business account is approved and has access to send messages.
- Ensure the recipient phone number has opted in to receive messages.

---

Feel free to contribute or raise issues if you find any bugs!

