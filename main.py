from gmail_api import Gmail
from calendar_api import Calendar 
from utils import DateTimeType, Utils
from excel import Excel

import os
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/calendar.readonly']


def main():
    
    config = Utils.openConfig()
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("")
    print(f"{'-'*20} Accessing Gmail ALL inbox {'-'*20}")
    print("\x1B[33m")
    gmail = Gmail(creds, config['email'], config['date'], DateTimeType[config['dateType']])
    gmail.getAllMessagesTillDate()
    inboxMails = gmail.getEmails()    
    print("\x1B[0m")
    print(f"{'-'*20} Gmail done {'-'*20}") 
    print("")
    
    print("")
    print(f"{'-'*20} Accessing Calendar Events {'-'*20}")
    print("\x1B[32m")
    calendar = Calendar(creds, config['email'], config['date'], DateTimeType[config['dateType']])
    calendarEmails = calendar.getEventsEmails()
    print("\x1B[0m")
    print(f"{'-'*20} Calednar done {'-'*20}") 
    print("")
    
    
    print("\x1B[34m")
    print(f"{'-'*20} Exporting to CSV File {'-'*20}")
    all_emails = inboxMails.union(calendarEmails)
        
    if config["csvName"] == "" or config["csvName"] is None:
        Excel(all_emails).extractCSV()
    else:
        Excel(all_emails).extractCSV(config["csvName"])
         
    print(f"{'-'*20} Exporting done {'-'*20}") 
    print("\x1B[0m")
    print("")
    
if __name__ == '__main__':
    main()