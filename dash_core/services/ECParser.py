from pprint import pprint
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
        self.event_classes_list = ["econoevents star", "econoevents djstar", "econoevents", "econoevents bullet"]
        self.table_day_classes = ["navwkday", "currentnavwkday"]
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
            return self.calendar_data
        else:
            raise CustomException(code=ExceptionCode.INTERNAL_SERVER_ERROR,
                                  message=ExceptionMessage.DASHCORE_URL_UNABLE_TO_PARSE_HTML)

    def _get_calendar_column_names(self, events: bs4.element.ResultSet) -> None:
        """
        Function for parsing and adding weekdays to final data structure

        :param events:
        :return:
        """
        table_data_days = events[0].find_all_next("td", {"class": self.table_day_classes})
        cnt = 0
        for table_data_day in table_data_days:
            self.calendar_data[cnt] = {"date": unidecode.unidecode(table_data_day.text), "events": []}
            cnt += 1
        if len(self.calendar_data) != 5:
            raise CustomException(code=ExceptionCode.INTERNAL_SERVER_ERROR,
                                  message=ExceptionMessage.DASHCORE_URL_UNABLE_TO_PARSE_WEEK)

    def _parse_calendar_column_data(self, events: bs4.element.ResultSet):
        econ_days = events[0].find_all_next("td", {"class": "events"})
        cnt = 0
        for econ_day in econ_days:
            econ_events = econ_day.find_all("div", {"class": self.event_classes_list})
            for econ_event in econ_events:
                event_name = unidecode.unidecode(econ_event.find_all("a")[0].text)
                event_time = unidecode.unidecode(econ_event.text.replace(event_name, '')).strip()
                self.calendar_data[cnt]["events"].append({"event_name": event_name,
                                                          "event_time": event_time,
                                                          "event_impact": self._event_impact_conventor(
                                                              econ_event.get("class"))})
            cnt += 1

    def _event_impact_conventor(self, event_type: list) -> int:
        if "star" in event_type:
            return 1
        elif "djstar" in event_type:
            return 2
        elif "bullet" in event_type:
            return 3
        else:
            return 4

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
pprint(parser.calendar_data[3])
