import csv
import datetime

class Excel(object):
    def __init__(self, emails) -> None:
        self._emails = emails
    
    def extractCSV(self, name=f"emails-{datetime.datetime.today().date()}") -> None:
        
        file = open(f"{name}.csv", 'w', newline='', encoding='utf-8')
        writer = csv.writer(file)

        for email in self._emails:
            writer.writerow([email])
        
        file.close()