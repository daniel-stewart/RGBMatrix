from  matrixBase import MatrixBase
from rgbmatrix import graphics
from icalendar import Calendar
import random

import requests
from requests.exceptions import HTTPError
from datetime import datetime, timedelta

# Add a secrets.py file to your project that has a dictionary
# called secrets with 'owmid' equal to your OpenWeatherMap ID.
try:
    from secrets import secrets
except ImportError:
    print("OWM Id is kept in secrets.py, please add them.")

class MatrixAB(MatrixBase):
    def __init__(self, number):
        self.level = number
        self.error = False
        self.extraSummary = ""

    def DrawBox(self, doubleBuffer, x0, y0, x1, y1, color, thickness=1):
        graphics.DrawLine(doubleBuffer, x0, y0, x0, y1, color)
        graphics.DrawLine(doubleBuffer, x0, y0, x1, y0, color)
        graphics.DrawLine(doubleBuffer, x1, y0, x1, y1, color)
        graphics.DrawLine(doubleBuffer, x0, y1, x1, y1, color)
        return

    def createOtherDay(self, doubleBuffer, num=0):
        if num == 0:
            self.DrawBox(doubleBuffer, 0, 0, 63, 31, graphics.Color(255, 255, 0))
            font = graphics.Font()
            font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/6x13.bdf")
            color = graphics.Color(0, 128, 128)
            graphics.DrawText(doubleBuffer, font, 14, 12, color, "Have a")
            graphics.DrawText(doubleBuffer, font, 6, 26, color, "Great Day")
        elif num == 1:
            self.DrawBox(doubleBuffer, 0, 0, 63, 31, graphics.Color(180, 250, 255))
            font = graphics.Font()
            font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/6x13.bdf")
            color = graphics.Color(255, 255, 0)
            graphics.DrawText(doubleBuffer, font, 14, 11, color, "Have a")
            graphics.DrawText(doubleBuffer, font, 18, 21, color, "Great")
            graphics.DrawText(doubleBuffer, font, 11, 30, color, "Weekend")
        elif num == 2:
            self.DrawBox(doubleBuffer, 0, 0, 63, 31, graphics.Color(255, 225, 77))
            font = graphics.Font()
            font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/6x13.bdf")
            color = graphics.Color(25, 217, 255)
            graphics.DrawText(doubleBuffer, font, 17, 11, color, "Enjoy")
            graphics.DrawText(doubleBuffer, font, 21, 21, color, "Your")
            graphics.DrawText(doubleBuffer, font, 11, 30, color, "Weekend")
        return True

    def createDay(self, day, doubleBuffer, color, num=0, extraSummary=""):
        doubleBuffer.Clear()
        if num == 3 and extraSummary == "":
            num = 1
        if num == 0 or num == 1:
            font = graphics.Font()
            font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/extra/LinLibertineB-42.bdf")
            graphics.DrawText(doubleBuffer, font, 3, 30, color, day)
            font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/7x13.bdf")
            yellow = graphics.Color(255,255,0)
            graphics.DrawText(doubleBuffer, font, 36, 24, yellow, "Day")
            if num == 1:
                graphics.DrawLine(doubleBuffer, 0, 0, 0, 31, yellow)
                graphics.DrawLine(doubleBuffer, 1, 0, 63, 0, yellow)
                graphics.DrawLine(doubleBuffer, 63, 1, 63, 31, yellow)
                graphics.DrawLine(doubleBuffer, 1, 31, 62, 31, yellow)
        elif num == 2:
            font = graphics.Font()
            font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/extra/Butler-ExtraBold-30.bdf")
            graphics.DrawText(doubleBuffer, font, 12, 32, color, day)
            font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/7x13.bdf")
            yellow = graphics.Color(255,255,0)
            white = graphics.Color(255,255,255)
            graphics.DrawText(doubleBuffer, font, 37, 28, white, "Day")
            graphics.DrawText(doubleBuffer, font, 4, 9, white, "Today is")
        elif num == 3:
            font = graphics.Font()
            font2 = graphics.Font()
            font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/extra/Butler-ExtraBold-30.bdf")
            graphics.DrawText(doubleBuffer, font, 12, 21, color, day)
            font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/6x13.bdf")
            font2.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/5x8.bdf")
            yellow = graphics.Color(255,255,0)
            white = graphics.Color(255,255,255)
            graphics.DrawText(doubleBuffer, font, 37, 17, yellow, "Day")
            graphics.DrawText(doubleBuffer, font2, 0, 31, white, extraSummary)
        print("Created", day)
        return

    def initialize(self, width, height, doubleBuffer):
        try:
            r = requests.get(secrets['schedule_url'])
            r.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTPError occurredL {http_err}')
            self.error = True
        except Exception as err:
            print(f'Other error occurred: {err}')
            self.error = True
        if self.error:
            f = graphics.Font()
            f.LoadFont('/home/pi/rpi-rgb-led-matrix/fonts/10x20.bdf')
            white = graphics.Color(255,255,255)
            graphics.DrawText(doubleBuffer, f, 8,22, white, "Hi !")
            graphics.DrawLine(doubleBuffer, 0, 0, 0, 31, white)
            graphics.DrawLine(doubleBuffer, 1, 0, 1, 31, white)
            graphics.DrawLine(doubleBuffer, 63, 0, 63, 31, white)
            graphics.DrawLine(doubleBuffer, 62, 0, 62, 31, white)
            graphics.DrawLine(doubleBuffer, 2, 0, 61, 0, white)
            graphics.DrawLine(doubleBuffer, 2, 1, 61, 1, white)
            graphics.DrawLine(doubleBuffer, 2, 30, 61, 30, white)
            graphics.DrawLine(doubleBuffer, 2, 31, 61, 31, white)
            return
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
                        color = graphics.Color(255, 30, 40)
                        display2 = "A"
                        print(self.summary)
                        self.createDay(display2, doubleBuffer, color, num=3, extraSummary=self.extraSummary)
                        return
                    elif self.summary == 'B' or self.summary.startswith('B Day'):
                        color = graphics.Color(20, 100, 255)
                        display2 = "B"
                        print(self.summary)
                        self.createDay(display2, doubleBuffer, color, num=3, extraSummary=self.extraSummary)
                        return
        doubleBuffer.Clear()
        num = 0
        if self.now.weekday() == 5 or self.now.weekday() == 6:
            num = random.randint(1,2)
        self.createOtherDay(doubleBuffer, num)
        return
    
    def restart(self, doubleBuffer):
        if self.error or self.now.hour != datetime.now().hour:
            try:
                print('Getting the calendar again')
                r = requests.get(secrets['schedule_url'])
                r.raise_for_status()
                self.error = False
            except HTTPError as http_err:
                print(f'HTTPError occurred: {http_err}')
                self.error = True
            except Exception as err:
                print(f'Other error occurred: {err}')
                self.error = True
            if self.error:
                f = graphics.Font()
                f.LoadFont('/home/pi/rpi-rgb-led-matrix/fonts/10x20.bdf')
                white = graphics.Color(255,255,255)
                graphics.DrawText(doubleBuffer, f, 8,22, white, "Hi !")
                graphics.DrawLine(doubleBuffer, 0, 0, 0, 31, white)
                graphics.DrawLine(doubleBuffer, 1, 0, 1, 31, white)
                graphics.DrawLine(doubleBuffer, 63, 0, 63, 31, white)
                graphics.DrawLine(doubleBuffer, 62, 0, 62, 31, white)
                graphics.DrawLine(doubleBuffer, 2, 0, 61, 0, white)
                graphics.DrawLine(doubleBuffer, 2, 1, 61, 1, white)
                graphics.DrawLine(doubleBuffer, 2, 30, 61, 30, white)
                graphics.DrawLine(doubleBuffer, 2, 31, 61, 31, white)
                return
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
                            color = graphics.Color(255, 30, 40)
                            display2 = "A"
                            print(self.summary)
                            self.createDay(display2, doubleBuffer, color, num=3, extraSummary=self.extraSummary)
                            return
                        elif self.summary == 'B' or self.summary.startswith('B Day'):
                            color = graphics.Color(20, 100, 255)
                            display2 = "B"
                            print(self.summary)
                            self.createDay(display2, doubleBuffer, color, num=3, extraSummary=self.extraSummary)
                            return
            doubleBuffer.Clear()
            num = 0
            if self.now.weekday() == 5 or self.now.weekday() == 6:
                num = random.randint(1,2)
            self.createOtherDay(doubleBuffer, num)
            return
        else:
            if self.summary == 'A' or self.summary.startswith('A '):
                color = graphics.Color(255, 30, 40)
                display2 = "A"
                print(self.summary)
                self.createDay(display2, doubleBuffer, color, num=3, extraSummary=self.extraSummary)
                return
            elif self.summary == 'B' or self.summary.startswith('B '):
                color = graphics.Color(20, 100, 255)
                display2 = "B"
                print(self.summary)
                self.createDay(display2, doubleBuffer, color, num=3, extraSummary=self.extraSummary)
                return
            doubleBuffer.Clear()
            num = 0
            if self.now.weekday() == 5 or self.now.weekday() == 6:
                num = random.randint(1,2)
            self.createOtherDay(doubleBuffer, num)
            return

    def run(self, doubleBuffer):
        return 0
