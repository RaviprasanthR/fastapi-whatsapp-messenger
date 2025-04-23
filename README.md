
# FastAPI WhatsApp Bot

This FastAPI application allows you to send WhatsApp messages using the WhatsApp Business API. The application accepts a phone number and sends a WhatsApp message using a pre-defined template.

## Features

- Send WhatsApp messages using templates.
- Handle rate limiting with retries using exponential backoff.
- Simple phone number validation (E.164 format).
- Logs all requests and responses for better debugging and tracking.

## Requirements

- Python 3.8+
- FastAPI
- Requests
- Python Dotenv

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/whatsapp-fastapi-bot.git
   cd whatsapp-fastapi-bot
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scriptsctivate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   - Create a `.env` file in the root of the project and add the following:
     ```
     WHATSAPP_API_VERSION=v17.0
     WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
     WHATSAPP_ACCESS_TOKEN=your_access_token
     ```

5. Run the FastAPI app:
   ```bash
   uvicorn main:app --reload
   ```

6. Access the documentation at:
   [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Endpoints

### `POST /send_message`

Sends a WhatsApp message to the specified phone number using a pre-defined template.

#### Request Body

```json
{
  "phone_number": "+1234567890"
}
```

#### Response

```json
{
  "status": "Message sent successfully",
  "whatsapp_response": {
    // Response data from WhatsApp API
  }
}
```

## Logging and Error Handling

The application logs all incoming requests and responses for better debugging and monitoring. If an error occurs (e.g., invalid phone number, WhatsApp API failure), appropriate error messages are returned.


