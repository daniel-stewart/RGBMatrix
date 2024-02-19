from icalendar import Calendar
import requests
from requests.exceptions import HTTPError
from datetime import datetime, timedelta

# Add a secrets.py file to your project that has a dictionary
# called secrets with 'owmid' equal to your OpenWeatherMap ID.
try:
    from secrets import secrets
except ImportError:
    print("OWM Id is kept in secrets.py, please add them.")

class UtilsAB:
    def __init__(self):
        self.day = ""
        self.summary = ''
        self.extraSummary = ''
        self.error = True
        self.now = datetime.now()

    def run(self):
        #print("Time to get A/B day")
        #print('self.error', self.error)
        #print('self.now', self.now.hour)
        #print('datetime.now().hour', datetime.now().hour)
        if self.error or self.now.hour != datetime.now().hour:
            print("Time to get A/B day")
            try:
                r = requests.get(secrets['schedule_url'])
                r.raise_for_status()
            except HTTPError as http_err:
                print(f'HTTPError occurred: {http_err}')
                self.error = True
                return False
            except Exception as err:
                print(f'Other error occurred: {err}')
                self.error = True
                return False
            self.error = False

            cal = Calendar.from_ical(r.content)
            self.now = datetime.now()

            print("Got calendar")
            for component in cal.walk():
                if component.name == "VEVENT":
                    self.summary = component.get('summary')
                    start = component.get('dtstart').dt
                    #print(summary)
                    if self.now.month == start.month and self.now.day == start.day:
                        print(self.summary)
                        self.extraSummary = ""
                        if self.summary.find("B Day 2") != -1 or self.summary.find("B Day 4") != -1 or self.summary.find("B Day 8") != -1:
                            self.extraSummary = "   Seminar"
                        elif self.summary.find("B Day 10") != -1:
                            self.extraSummary = "Convocation"
                        elif self.summary.find("B Day 6") != -1:
                            self.extraSummary = "Math Testing"
                        elif self.summary.find("2 HR delay") != -1:
                            self.extraSummary = "2 Hour Delay"
                        elif self.summary.find("1 HR delay") != -1:
                            self.extraSummary = "1 Hour Delay"
                        elif self.summary.find("SAT Testing") != -1:
                            self.extraSummary = "SAT Testing"
                        #extraSummary = "    Seminar"
                        if self.summary == 'A' or self.summary.startswith('A Day'):
                            self.day = "A"
                            print(self.summary)
                            return True
                        elif self.summary == 'B' or self.summary.startswith('B Day'):
                            self.day = "B"
                            print(self.summary)
                            return True
            if self.now.weekday() == 5 or self.now.weekday() == 6:
                self.day = ""
            return True
        return True
    
    def getDay(self):
        return self.day
    
    def getSummary(self):
        return self.summary
    
    def getExtraSummary(self):
        return self.extraSummary