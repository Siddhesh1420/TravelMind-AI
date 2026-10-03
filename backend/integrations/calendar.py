import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from config.settings import GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, GOOGLE_REDIRECT_URI

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

# In-memory token store (replace with DB later)
user_tokens = {}

def get_google_flow():
    return Flow.from_client_secrets_file(
        'credentials.json',
        scopes=SCOPES,
        redirect_uri=GOOGLE_REDIRECT_URI
    )

flow_store = {}

def get_auth_url():
    flow = get_google_flow()
    auth_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent'
    )
    # Store flow with state as key
    flow_store[state] = flow
    return auth_url, state

def exchange_code_for_token(code: str, state: str, user_id: str):
    # Get the stored flow
    flow = flow_store.get(state)
    if not flow:
        # Fallback — create new flow
        flow = get_google_flow()
    
    flow.fetch_token(code=code)
    credentials = flow.credentials
    
    # Store token
    user_tokens[user_id] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': list(credentials.scopes) if credentials.scopes else []
    }
    
    # Cleanup
    if state in flow_store:
        del flow_store[state]
    
    return credentials

def create_calendar_events(user_id: str, calendar_events: list) -> bool:
    try:
        if user_id not in user_tokens:
            print(f"No token found for user {user_id}")
            return False

        token_data = user_tokens[user_id]
        credentials = Credentials(
            token=token_data['token'],
            refresh_token=token_data['refresh_token'],
            token_uri=token_data['token_uri'],
            client_id=token_data['client_id'],
            client_secret=token_data['client_secret'],
            scopes=token_data['scopes']
        )

        service = build('calendar', 'v3', credentials=credentials)

        for event in calendar_events:
            service.events().insert(
                calendarId='primary',
                body={
                    'summary': event.get('title', 'Trip Day'),
                    'description': event.get('description', ''),
                    'start': {
                        'date': event.get('date'),
                        'timeZone': 'Asia/Kolkata'
                    },
                    'end': {
                        'date': event.get('date'),
                        'timeZone': 'Asia/Kolkata'
                    }
                }
            ).execute()
            print(f"Created event: {event.get('title')}")

        return True

    except Exception as e:
        print(f"Calendar error: {e}")
        return False