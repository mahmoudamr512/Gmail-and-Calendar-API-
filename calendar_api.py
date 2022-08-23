from googleapiclient.discovery import build
from utils import DateTimeType, Utils
import json
import datetime

class Calendar(object):
    def __init__(self, creds, email, date, datetype) -> None:
        self._email = email
        self._date = Utils(date).normalizeDate(datetype)    
        self._creds = creds
        self.service = build('calendar', 'v3', credentials=self._creds)
        self.calendar_ids = self._getAllCalendars()
        
    def _getAllCalendars(self) -> list:
        calendar_ids = []
        for calendar in  self.service.calendarList().list(maxResults=250).execute()["items"]:
            calendar_ids.append(calendar["id"])
        return calendar_ids

    def getEventsEmails(self):
        print(f'{"-" * 20} Getting all  Emails for Events since {self._date} {"-" * 20}')
        returnMails = set()
        
        for id in self.calendar_ids:
            events = self.service.events().list(calendarId=id, 
                    maxResults=2500, 
                    timeMin=datetime.datetime.strptime(self._date, "%Y/%m/%d").astimezone().isoformat('T'),
                    timeMax=datetime.datetime.now().astimezone().isoformat('T')).execute()["items"]
            
            for event in events:
                emails = self._extractMails(event)
                
                for email in emails:
                    returnMails.add(email)
        
        print(f'{"-" * 20} Found {len(returnMails)} Emails in Events since {self._date} {"-" * 20}')
        return returnMails
    
    def _extractMails(self, event):
        emails = set()

        if "organizer" in event:
            emails.add(event["organizer"]["email"])
            
        if "attendees" in event:
            for attendant in event["attendees"]:
                emails.add(attendant["email"])
                
        return emails
    


