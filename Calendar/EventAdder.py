import json
from datetime import datetime, timedelta
from google.oauth2 import service_account
from googleapiclient.discovery import build
import logging

from calendar_event import CalendarEvent

# Set up logging
logging.basicConfig(level=logging.INFO)

class GoogleCalendarEventAdder:
    def __init__(self, config_file):
        """
        Initializes the GoogleCalendarEventAdder with a configuration file.

        Parameters:
        config_file (str): The path to the configuration JSON file.
        """
        self.config = self.load_config(config_file)
        self.calendar_id = self.config['calendar_id']
        self.credentials_file = self.config['credentials_file']
        self.timezone = self.config['timezone']
        self.credentials = self.load_credentials(self.credentials_file)
        self.service = self.build_service(self.credentials)

    def load_config(self, config_file):
        """
        Loads the configuration from a JSON file.

        Parameters:
        config_file (str): The path to the configuration JSON file.

        Returns:
        dict: The configuration dictionary.
        """
        with open(config_file, 'r') as f:
            config = json.load(f)
        return config

    def load_credentials(self, credentials_file):
        """
        Loads the credentials from the JSON file.

        Parameters:
        credentials_file (str): The path to the Google API credentials JSON file.

        Returns:
        service_account.Credentials: The loaded credentials.
        """
        credentials = service_account.Credentials.from_service_account_file(credentials_file, scopes=['https://www.googleapis.com/auth/calendar'])
        logging.info("Credentials loaded successfully")
        return credentials

    def build_service(self, credentials):
        """
        Builds the Google Calendar service object.

        Parameters:
        credentials (service_account.Credentials): The credentials for Google API.

        Returns:
        Resource: The Google Calendar service object.
        """
        service = build('calendar', 'v3', credentials=credentials)
        logging.info("Google Calendar service built successfully")
        return service

    def add_events_to_calendar(self, events):
        """
        Adds a list of events to Google Calendar.

        Parameters:
        events (list): A list of CalendarEvent objects

        Returns:
        None
        """
        try:
            for event in events:
                created_event = event.to_google_format()

                # Insert the event into the calendar
                created_event = self.service.events().insert(calendarId=self.calendar_id, body=event).execute()
                logging.info(f"Event created: {created_event.get('htmlLink')}")
                logging.info(f"Event details: {created_event}")

        except Exception as e:
            logging.error(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    # Initialize the event adder with the configuration file
    config_file = 'secrets.json'
    event_adder = GoogleCalendarEventAdder(config_file)

    # Example event data
    events = [
        CalendarEvent(
            summary='Meeting with Team',
            start_datetime=datetime(2024, 7, 10, 9, 0),
            end_datetime=datetime(2024, 7, 10, 10, 0),
            color_id='1'
        )   
    ]
    # Add events to Google Calendar
    event_adder.add_events_to_calendar(events)
