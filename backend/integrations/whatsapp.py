from twilio.rest import Client
import os
import json 

def send_whatsapp_message(to_number: str, message: str) -> bool:
    """
    Send WhatsApp message via Twilio
    to_number: user's phone number with country code (e.g. +919876543210)
    message: the whatsapp_message from writer agent
    """
    try:
        account_sid = os.getenv("TWILIO_ACCOUNT_SID")
        auth_token = os.getenv("TWILIO_AUTH_TOKEN")
        from_number = os.getenv("TWILIO_WHATSAPP_NUMBER")
        
        print(f"SID: {account_sid[:10]}...")
        print(f"Token length: {len(auth_token) if auth_token else 0}")
        print(f"From: {from_number}")

        client = Client(account_sid, auth_token)

        msg = client.messages.create(
        from_=f"whatsapp:{from_number}",
        to=f"whatsapp:{to_number}",
        content_sid="HXb5b62575e6e4ff6129ad7c8efe1f983e",
        content_variables=json.dumps({"1": "TravelMind AI", "2": "Your trip is ready!"})
    )

        print(f"WhatsApp message sent: {msg.sid}")
        return True

    except Exception as e:
        print(f"WhatsApp error type: {type(e)}")
        print(f"WhatsApp error: {e}")
        return False