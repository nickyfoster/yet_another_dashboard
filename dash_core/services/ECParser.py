import bs4
import requests
import unidecode

from dash_core.services.Exception import CustomException
from dash_core.services.ExceptionCode import ExceptionCode
from dash_core.services.ExceptionMessage import ExceptionMessage


class ECParser:
    """
    Econ Calendar parsing logic.
    """
    def __init__(self, url=None):
        self.url = url if url else "https://ibd.econoday.com/byweek.asp?cust=ibd&cty=US&lid=0"
        self.calendar_data = dict()
        self.html_text = self.get_html_text(self.url)
        if self.html_text:
            self.soup = bs4.BeautifulSoup(markup=self.html_text, features='html.parser')

    def get_econ_calendar(self) -> dict:
        """Economic Calendar parser. We get main table from HTML source and split into two parts:
        1. Days. Here we get weekdays and their numbers.
        2. Events. Here we get economic events with time and description.
        :return: dict, calendar_data
        """
        events = self.soup.find_all("table", {"class": "eventstable"})
        if len(events) == 1:
            self._get_calendar_column_names(events)
            self._parse_calendar_column_data(events)
        else:
            raise CustomException(code=ExceptionCode.INTERNAL_SERVER_ERROR,
                                  message=ExceptionMessage.DASHCORE_URL_UNABLE_TO_PARSE_HTML)

    def _get_calendar_column_names(self, events: bs4.element.ResultSet):
        table_data_days = events[0].find_all_next("td", {"class": ["navwkday", "currentnavwkday"]})
        for table_data_day in table_data_days:
            self.calendar_data[unidecode.unidecode(table_data_day.text)] = None
        if len(self.calendar_data) != 5:
            raise CustomException(code=ExceptionCode.INTERNAL_SERVER_ERROR,
                                  message=ExceptionMessage.DASHCORE_URL_UNABLE_TO_PARSE_WEEK)

    def _parse_calendar_column_data(self, events: bs4.element.ResultSet):
        table_data_events = events
        print(events)

    @staticmethod
    def get_html_text(url):
        try:
            result = requests.get(url).text
        except Exception:
            raise CustomException(code=ExceptionCode.BAD_REQUEST,
                                  message=ExceptionMessage.DASHCORE_URL_INVALID)
        return result


parser = ECParser()
parser.get_econ_calendar()
