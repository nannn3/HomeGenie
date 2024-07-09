from datetime import datetime, timedelta
import json

CONFIG_FILE = 'secrets.json'

class CalendarEvent:
    def __init__(self, summary, start_datetime, end_datetime=None, color_id=None):
        """
        Initializes a CalendarEvent object.

        Parameters:
        summary (str): Summary or title of the event.
        start_datetime (datetime): Start date and time of the event.
        end_datetime (datetime, optional): End date and time of the event. If not provided, defaults to one hour after the start time.
        color_id (str, optional): Color ID for the event.
        """
        self.summary = summary
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime if end_datetime else start_datetime + timedelta(hours=1)
        self.color_id = color_id
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            self.timezone = config['timezone']

    # Getter and Setter for summary
    @property
    def summary(self):
        return self._summary

    @summary.setter
    def summary(self, value):
        self._summary = value

    # Getter and Setter for start_datetime
    @property
    def start_datetime(self):
        return self._start_datetime

    @start_datetime.setter
    def start_datetime(self, value):
        self._start_datetime = value

    # Getter and Setter for end_datetime
    @property
    def end_datetime(self):
        return self._end_datetime

    @end_datetime.setter
    def end_datetime(self, value):
        self._end_datetime = value

    # Getter and Setter for color_id
    @property
    def color_id(self):
        return self._color_id

    @color_id.setter
    def color_id(self, value):
        self._color_id = value

    def to_google_format(self):
        """
        Converts the event data to the format expected by Google Calendar.

        Parameters:
        None

        Returns:
        dict: A dictionary representing the event in Google Calendar format.
        """
        event = {
            'summary': self.summary,
            'start': {
                'dateTime': self.start_datetime.isoformat(),
                'timeZone': self.timezone,
            },
            'end': {
                'dateTime': self.end_datetime.isoformat(),
                'timeZone': self.timezone,
            },
            'visibility': 'default'
        }

        if self.color_id:
            event['colorId'] = self.color_id

        return event

if __name__ == '__main__':
    event = CalendarEvent(
    summary='Meeting with Team',
    start_datetime=datetime(2024, 7, 10, 9, 0),
    end_datetime=datetime(2024, 7, 10, 10, 0),
    color_id='1'
    )
    print (event.timezone)
    print (event.to_google_format()) 
