from googleapiclient.discovery import build
from utils import DateTimeType, Utils
import json

class Gmail(object):
    def __init__(self, creds, email, date, datetype) -> None:
        self._email = email
        self._date = Utils(date).normalizeDate(datetype)    
        self._creds = creds
        self.messages = []
        self.service = build('gmail', 'v1', credentials=self._creds)

    def getAllMessagesTillDate(self) -> list:
        print("")
        print(f'{"-" * 20} Getting all messages since {self._date} {"-" * 20}')
        # Call the Gmail API
        messages_rqst = self.service.users().messages().list(userId=self._email, q=f'in:anywhere after:{self._date}')
        messages_resp = None
        
        try:
            messages_resp = messages_rqst.execute()
        except: 
            pass
        
        while messages_resp is not None:
            msgs = messages_resp["messages"]
            
            for msg in msgs:
                self.messages.append(msg)
                
            try:
                messages_rqst = self.service.users().messages().list_next(previous_request = messages_rqst, previous_response = messages_resp)
                messages_resp = messages_rqst.execute()
            except:
                break    
        print(f"{'-' * 20} Found {len(self.messages)} Email Messages since {self._date} {'-' * 20}")

    def getEmails(self):
        print(f"{'-' * 20} Extracting emails {'-' * 20}")
        emails = set()
        for msg in self.messages:
            message = self.service.users().messages().get(userId=self._email, id=msg['id']).execute()
            
            headers = message["payload"]["headers"]
            
            for header in headers:
                if header["name"] == "To" or  header["name"] == "Cc" or  header["name"] == "Bcc":
                    for email in Utils.extractEmail(header["value"]):
                        emails.add(email) 
        print(f"{'-' * 20} Found {len(emails)} emails {'-' * 20}")
        return emails
    


