import requests
from bs4 import BeautifulSoup
import unidecode
from requests.exceptions import MissingSchema

from dash_core.services.Exception import CustomException
from dash_core.services.ExceptionCode import ExceptionCode
from dash_core.services.ExceptionMessage import ExceptionMessage


class ECParser:
    def __init__(self, url=None):
        self.url = url if url else "https://ibd.econoday.com/byweek.asp?cust=ibd&cty=US&lid=0"
        self.html_text = self.get_html_text(self.url)
        if self.html_text:
            self.soup = BeautifulSoup('html.parser')

    def parse_calendar(self):
        events = self.soup.find_all("table", {"class": "eventstable"})
        calendar_data = {}
        if len(events) == 1:
            table_days_names = events[0].find_all_next("td", {"class": ["navwkday", "currentnavwkday"]})
            for table_days_name in table_days_names:
                calendar_data[unidecode.unidecode(table_days_name.text)] = None
                print(table_days_name.text)

    @staticmethod
    def get_html_text(url):
        try:
            res = requests.get(url).text
            return res
        except MissingSchema:
            raise CustomException(code=ExceptionCode.BAD_REQUEST,
                                  message=ExceptionMessage.DASHCORE_URL_INVALID)


parser = ECParser(url="ass")
print(parser.url)
