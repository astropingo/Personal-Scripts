import os.path
import datetime
import argparse
from enum import Enum

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class Conf(Enum):
    CALENDAR_ID = "" # Calendar ID, found on Google Calendar settings
    TIME_ZONE = "" # Timezone. e.g. America/Sao_Paulo
    REMINDERS_MINUTES = 1440 # Reminder time in minutes. Default: 1440 (24 hours)
    COLOR_ID = 2 # Color ID. Default: 2 (Green)
    # If modifying these scopes, delete the file token.json.
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    if CALENDAR_ID == "":
        raise ValueError("CALENDAR_ID cannot be empty.")
    if TIME_ZONE == "":
        raise ValueError("TIME_ZONE cannot be empty.")

def create_recurring_event(calendar_service, name, date, description, conf):
    date = "-".join([x.zfill(2) for x in date.replace("/", "-").split("-")])
    current_year = datetime.datetime.now().year
    start_date = datetime.datetime.strptime(f"{current_year}-{date}", "%Y-%d-%m").date()
    end_date = start_date + datetime.timedelta(days=1)

    event = {
        'summary': f"Aniversário: {name}",
        "colorId": conf.COLOR_ID.value,
        "description": description,
        'start': {
            'date': start_date.isoformat(),
            'timeZone': conf.TIME_ZONE.value,
        },
        'end': {
            'date': end_date.isoformat(),
            'timeZone': conf.TIME_ZONE.value,
        },
        'recurrence': [
            'RRULE:FREQ=YEARLY'
        ],
        "reminders.overrides[].minutes": conf.REMINDERS_MINUTES.value,
        "transparency": "transparent",
    }
    event = calendar_service.events().insert(calendarId=conf.CALENDAR_ID.value, body=event).execute()
    print(f'Event created: {event.get("htmlLink")}')

def main():
    parser = argparse.ArgumentParser(description='Adiciona um aniversário ao Google Calendar')
    parser.add_argument('name', help='Nome')
    parser.add_argument('date', help='Data do Aniversário (DD-MM)')
    parser.add_argument('description', help="Descrição (opcional)", nargs='?', default="")
    args = parser.parse_args()

    creds = None
    conf = Conf
    # Generate the token.json on Google API developer console
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', conf.SCOPES.value)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', conf.SCOPES.value)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('calendar', 'v3', credentials=creds)
    except HttpError as error:
        print('An error occurred: %s' % error)

    create_recurring_event(service, args.name, args.date, args.description, conf)

if __name__ == '__main__':
    main()