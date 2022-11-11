import json
import time

import bs4
import unidecode

from dashcore.services.Exception import CustomException
from dashcore.services.ExceptionCode import ExceptionCode
from dashcore.services.ExceptionMessage import ExceptionMessage
from dashcore.services.bashcore_config import ECParserConfig
from dashcore.utils.utils import event_impact_convertor, get_html_text, date_converter, get_db_connector


class ECParser:
    """
    Econ Calendar parsing logic.
    """

    def __init__(self, config: ECParserConfig):
        self.config = config
        self.url = self.config.url
        self.cache_enabled = self.config.cache_enabled
        self.redis = get_db_connector()
        self.calendar_data = dict()
        self.event_classes_list = ["econoevents star", "econoevents djstar", "econoevents", "econoevents bullet"]
        self.table_day_classes = ["navwkday", "currentnavwkday"]
        self.redis_cache_var_name = "ecparser/chache/data"

    def get_econ_data(self):
        if self.cache_enabled:
            raw_data = self.redis.get(self.redis_cache_var_name)
            if raw_data:
                econ_data = json.loads(raw_data)
                data_ttl = econ_data.get('ts')
                if time.time() - data_ttl < self.config.update_period_seconds:
                    return econ_data.get("data")
                else:
                    calendar_data = self._get_econ_data()
                    self.renew_cache(calendar_data)
                    return calendar_data
            else:
                calendar_data = self._get_econ_data()
                self.renew_cache(calendar_data)
                return calendar_data
        else:
            return self._get_econ_data()

    def renew_cache(self, calendar_data):
        redis_data = {"ts": time.time(), "data": calendar_data}
        self.redis.set(self.redis_cache_var_name, json.dumps(redis_data))

    def _get_econ_data(self) -> dict:
        """Economic Calendar parser. We get main table from HTML source and split into two parts:
        1. Days. Weekdays and their numbers.
        2. Events. Economic events with time and description.
        :return: dict, calendar_data
        """
        html_text = get_html_text(self.url)
        if html_text:
            soup = bs4.BeautifulSoup(markup=html_text, features='html.parser')
        events = soup.find_all("table", {"class": "eventstable"})
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
            date = unidecode.unidecode(table_data_day.text)
            self.calendar_data[cnt] = {"date": date_converter(date), "events": []}
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
                                                          "event_impact": event_impact_convertor(
                                                              econ_event.get("class"))})
            cnt += 1


if __name__ == '__main__':
    from dashcore.utils.utils import get_config
    from pprint import pprint

    econ_calendar = ECParser(get_config().ECParser).get_econ_data()
    pprint(f"Econ_data: {econ_calendar}")
