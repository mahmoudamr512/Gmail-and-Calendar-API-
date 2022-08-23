from datetime import datetime, date, timedelta 
from enum import Enum
from dateutil import parser
import re
from jsonc_parser.parser import JsoncParser


class DateTimeType(Enum):
    DAY_MONTH_YEAR = "%d-%m-%Y"
    DAY_MONTH_YEAR_SLASH = "%d/%m/%Y"
    MONTH_DAY_YEAR = "%m-%d-%Y"
    MONTH_DAY_YEAR_SLASH = "%m/%d/%Y"
    YEAR_MONTH_DAY = "%y-%m-%d"
    YEAR_MONTH_DAY_SLASH = "%y/%m/%d"
    YEAR_DAY_MONTH = "%y-%d-%m"
    YEAR_DAY_MONTH_SLASH = "%y/%d/%m"
    DAYS = 1
    MONTHS = 2
    GMAIL_DATE = 3


class Utils(object):
    
    def __init__(self, inputDate=None) -> None:
        self._date = inputDate
    
    @staticmethod
    def extractEmail(emailString) -> str:
        return re.findall(r'[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}', emailString)
    
    @staticmethod
    def openConfig() -> dict:
        return JsoncParser.parse_file('config.jsonc')
    
    def normalizeDate(self, dateType) -> datetime:
        """
        Change any date format to a normalized datetime.    
        """
        if dateType.name != 'DAYS' and dateType.name != 'MONTHS':
            if dateType.name == 'GMAIL_DATE':
                return parser.parse(self._date).date().strftime("%Y/%m/%d")
            else:
                return datetime.strptime(self._date, dateType.value).date().strftime("%Y/%m/%d")
        else:
            if dateType.name == 'DAYS':
                numberOfDays = int(self._date.replace('d', '').replace('D', '').replace(' ', ''))
                return (date.today() - timedelta(days=numberOfDays)).strftime("%Y/%m/%d")
            else:
                numberOfMonths = int(self._date.replace('m', '').replace('M', '').replace(' '))
                return (date.today() - timedelta(days=2, weeks=4)).strftime("%Y/%m/%d")
    
    @staticmethod
    def isLessThenDate(datetime1, datetime2) -> bool:
        """
        Compare and return if datetime1 is less than datetime2.
        
        Args:
            datetime1 (datetime): First Date
            datetime2 (datetime): Second Date

        Returns:
            bool: Return a boolean if datetime1 is less than datetime2.
        """
        return datetime1 < datetime2
    