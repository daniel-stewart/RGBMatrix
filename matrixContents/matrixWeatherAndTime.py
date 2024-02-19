from matrixBase import MatrixBase
from rgbmatrix import graphics
from PIL import Image
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from datetime import datetime
from datetime import timedelta
from utilsAB import UtilsAB

# Add a secrets.py file to your project that has a dictionary
# called secrets with 'owmid' equal to your OpenWeatherMap ID.
try:
    from secrets import secrets
except ImportError:
    print("OWM Id is kept in secrets.py, please add them.")
    bSecretFileExists = False

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 128, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
BLUE_WHITE = (128, 128, 255)
DARK_BLUE = (0, 0, 128)

class MatrixWeatherAndTime(MatrixBase):
    def __init__(self, number):
        self.number = number
        self.bSecretFileExists = True
        self.OWMError = False
        self.weatherYOffset = 0 if self.number == 0 else 32
        self.wid = 0
        self.currentTemp = 0
    
    def colorRamp(self, temp):
        if temp < 45:
            return BLUE_WHITE
        elif temp > 80:
            return ORANGE
        else:
            if temp >= 65:
                green = int(((temp - 65.0) / 15.0) * 128.0)
                return tuple((255, 255 - green, 0))
            else:
                red = green = int(((temp - 45.0) / 20.0) * 128.0)
                blue = int(((temp - 45.0) / 20.0) * 255.0)
                return tuple((128 + red, 128 + green, 255 - blue))

    def createDay(self, day, doubleBuffer, color):
        font = graphics.Font()
        font.LoadFont(self.fontPathPrefix + "10x20.bdf")
        graphics.DrawText(doubleBuffer, font, 10, 20 + self.weatherYOffset, color, day)
        return
    
    def loadFonts(self):
        self.font = graphics.Font()
        self.font7x14 = graphics.Font()
        self.fontTimesRoman = graphics.Font()
        self.fontTimesRoman18 = graphics.Font()
        self.fontSmall = graphics.Font()
        self.fontLarge = graphics.Font()
        self.font6x13 = graphics.Font()

        self.font7x14.LoadFont(self.fontPathPrefix + "7x14.bdf")
        # The numbers & capital letters on a 10x20 font only use 13 pixels in height.
        self.font.LoadFont(self.fontPathPrefix + "10x20.bdf")
        # This Times Roman font is 13x17 pixels on capital 'M', and goes 4 pixels beneath baseline on 'q'
        self.fontTimesRoman.LoadFont(self.fontPathPrefix + "extra/75dpi/timR14.bdf")
        self.fontTimesRoman18.LoadFont(self.fontPathPrefix + "extra/75dpi/timR18.bdf")
        self.fontSmall.LoadFont(self.fontPathPrefix + "5x8.bdf")
        self.fontLarge.LoadFont(self.fontPathPrefix + "extra/75dpi/ncenR18.bdf")
        self.font6x13.LoadFont(self.fontPathPrefix + "6x13.bdf")
    
    def drawTime(self, doubleBuffer, count=0):
        if count == 0:
            self.timeYOffset = 0
            currentTime = self.timeNow.strftime("%-I:%M")
            currentMonth = self.timeNow.strftime("%b %d")
            offset = 13
            if self.timeNow.hour%12 == 0 or self.timeNow.hour%12 > 9:
                offset = 3
            length = graphics.DrawText(doubleBuffer, self.font7x14, 2, 12 + self.timeYOffset, graphics.Color(225, 255, 0), currentMonth)
            length = graphics.DrawText(doubleBuffer, self.fontTimesRoman, offset, 28 + self.timeYOffset, graphics.Color(0, 255, 0), currentTime)
        elif count == 1:
            currentTime = self.timeNow.strftime("%-I:%M")
            currentMonth = self.timeNow.strftime("%b %d")
            offset = 18
            if self.timeNow.hour%12 == 0 or self.timeNow.hour%12 > 9:
                offset = 13
            length = graphics.DrawText(doubleBuffer, self.font6x13, 14, 13, graphics.Color(255, 128, 0), currentMonth)
            length = graphics.DrawText(doubleBuffer, self.fontTimesRoman, offset, 33, graphics.Color(0, 255, 0), currentTime)
        elif count == 2:
            currentTime = self.timeNow.strftime("%-I:%M")
            currentMonth = self.timeNow.strftime("%m/%d")
            offset = 13
            if self.timeNow.hour%12 == 0 or self.timeNow.hour%12 > 9:
                offset = 4
            length = graphics.DrawText(doubleBuffer, self.fontSmall, 21, 11, graphics.Color(0, 128, 0), currentMonth)
            length = graphics.DrawText(doubleBuffer, self.fontLarge, offset, 36, graphics.Color(255, 255, 255), currentTime)
        elif count == 3:
            currentTime = self.timeNow.strftime("%-I:%M")
            currentMonth = self.timeNow.strftime("%b %d")
            offset = 3
            if self.timeNow.hour%12 == 0 or self.timeNow.hour%12 > 9:
                offset = 3
            length = graphics.DrawText(doubleBuffer, self.font7x14, 3, 15, graphics.Color(255, 128, 0), currentMonth)
            length = graphics.DrawText(doubleBuffer, self.font, offset, 37, graphics.Color(0, 255, 0), currentTime)
        elif count == 4:
            currentTime = self.timeNow.strftime("%-I:%M")
            currentMonth = self.timeNow.strftime("%m/%d")
            offset = 12
            if self.timeNow.hour%12 == 0 or self.timeNow.hour%12 > 9:
                offset = 7
            length = graphics.DrawText(doubleBuffer, self.font6x13, 33, 14, graphics.Color(255, 128, 0), currentMonth)
            length = graphics.DrawText(doubleBuffer, self.fontTimesRoman18, offset, 41, graphics.Color(0, 255, 0), currentTime)
        return
    
    def drawABDay(self, doubleBuffer, text, count = 0):
        if text == 'A' or text == 'B':
            if count == 0:
                red = graphics.Color(*RED)
                white = graphics.Color(*WHITE)
                orange = graphics.Color(*ORANGE)
                graphics.DrawLine(doubleBuffer, 44, 0, 44, 33, orange)
                graphics.DrawLine(doubleBuffer, 44, 33, 63, 33, orange)
                graphics.DrawText(doubleBuffer, self.fontSmall, 47, 32, white, "Day")
                graphics.DrawText(doubleBuffer, self.fontLarge, 45, 21, red, text)
            elif count == 1:
                red = graphics.Color(*RED)
                white = graphics.Color(*WHITE)
                graphics.DrawText(doubleBuffer, self.fontLarge, 14, 60, red, text)
                graphics.DrawText(doubleBuffer, self.font6x13, 35, 59, white, "Day")
            elif count == 2:
                red = graphics.Color(*RED)
                blue = graphics.Color(*BLUE)
                if text == 'A':
                    graphics.DrawText(doubleBuffer, self.fontTimesRoman, 2, 14, red, 'A')
                elif text == 'B':
                    graphics.DrawText(doubleBuffer, self.fontTimesRoman, 52, 14, blue, 'B')
            elif count == 3:
                red = graphics.Color(*RED)
                white = graphics.Color(*WHITE)
                graphics.DrawText(doubleBuffer, self.font, 3, 60, red, text)
                graphics.DrawText(doubleBuffer, self.font7x14, 20, 60, graphics.Color(255, 255, 255), "Day")
            elif count == 4:
                red = graphics.Color(*RED)
                graphics.DrawText(doubleBuffer, self.font6x13, 2, 14, red, text)
                #graphics.DrawText(doubleBuffer, self.font6x13, 9, 14, graphics.Color(255, 255, 255), "day")
        return
    
    def drawWeather(self, doubleBuffer, count=0):
        if not self.OWMError:
            if count == 0:
                icon = self.iconPathPrefix + self.weatherTable[self.wid][0]
                image = Image.open(icon).convert('RGB')
                doubleBuffer.SetImage(image,0, self.weatherYOffset)
                graphics.DrawText(doubleBuffer, self.font, 35, 18 + self.weatherYOffset, graphics.Color(*self.colorRamp(self.currentTemp)), str(self.currentTemp)+"\u00B0")
                graphics.DrawText(doubleBuffer, self.font6x13, 0, 30 + self.weatherYOffset, graphics.Color(*WHITE), self.weatherTable[self.wid][1])
            elif count == 1:
                pass
            elif count == 2:
                icon = self.iconPathPrefix + self.weatherTable[self.wid][0]
                image = Image.open(icon).convert('RGB')
                doubleBuffer.SetImage(image,8, 39)
                graphics.DrawText(doubleBuffer, self.font7x14, 39, 58, graphics.Color(*self.colorRamp(self.currentTemp)), str(self.currentTemp)+"\u00B0")
            elif count == 3:
                graphics.DrawText(doubleBuffer, self.fontSmall, 49, 11, graphics.Color(*self.colorRamp(self.currentTemp)), str(self.currentTemp)+"\u00B0")
            elif count == 4:
                graphics.DrawText(doubleBuffer, self.font7x14, 43, 62, graphics.Color(*self.colorRamp(self.currentTemp)), str(self.currentTemp)+"\u00B0")
        return
    
    def getWeather(self):
        try:
            self.owm = OWM(secrets['owmid'])
            self.mgr = self.owm.weather_manager()
            observation = self.mgr.weather_at_place(secrets['owm_place'])
            w = observation.weather
            self.wid = w.weather_code
            #status = w.detailed_status
            temp = w.temperature('fahrenheit') # {'temp_max':10.5, 'temp':9.7, 'temp_min':4.5}
            self.currentTemp = round(temp['temp'])
            self.weatherNow = datetime.now() + timedelta(minutes=10)
        except Exception as err:
            print(f'Other error occurred: {err}')
            self.OWMError = True

    def initialize(self, width, height, doubleBuffer):
        self.iconPathPrefix = secrets['weatherIcondir_prefix'] # Original: '/home/pi/icons/weatherIcons/png/24x24/'
        self.fontPathPrefix = secrets['fontdir_prefix']
        self.ab = UtilsAB()
        self.weatherTable = {
            200:['012-rain-2.png','Thndr storm','Thunderstorm with light rain'],
            201:['012-rain-2.png','Thndr storm','Thunderstorm with rain'],
            202:['012-rain-2.png','Thndr storm','Thunderstorm with heavy rain'],
            210:['021-storm-1.png','Thndr storm','Light thunderstorm'],
            211:['021-storm-1.png','Thndr storm','Thunderstorm'],
            212:['041-storm.png','Thndr storm','Heavy thunderstorm'],
            221:['041-storm.png','Thndr storm','Ragged thunderstorm'],
            230:['012-rain-2.png','Thndr storm','Thunderstorm with light drizzle'],
            231:['012-rain-2.png','Thndr storm','Thunderstorm with drizzle'],
            232:['012-rain-2.png','Thndr storm','Thunderstorm with heavy drizzle'],
            300:['037-umbrella.png','Lt Drizzle','Light intensity drizzle'],
            301:['038-rain-1.png',  '   Drizzle','Drizzle'],
            302:['036-umbrella-1.png','   Drizzle','Heavy intensity drizzle'],
            310:['036-umbrella-1.png','   Drizzle','Light intensity drizzle rain'],
            311:['036-umbrella-1.png','   Drizzle','Drizzle rain'],
            312:['036-umbrella-1.png','   Drizzle','Heavy intensity drizzle rain'],
            313:['040-rain.png',   '    Drizzle','Shower rain and drizzle'],
            314:['036-umbrella-1.png','   Drizzle','Heavy shower rain and drizzle'],
            321:['036-umbrella-1.png','   Drizzle','Shower drizzle'],
            500:['002-drop.png',    'Light Rain','Light rain'],
            501:['010-rain-3.png',  '      Rain','Moderate rain'],
            502:['040-rain.png',    'Heavy Rain','Heavy intensity rain'],
            503:['040-rain.png',    'Heavy Rain','Very heavy rain'],
            504:['040-rain.png',    'Extrm. Rain','Extreme rain'],
            511:['010-rain-3.png',  '      Rain','Freezing rain'],
            520:['010-rain-3.png',  '      Rain','Light intensity shower rain'],
            521:['010-rain-3.png',  '      Rain','Shower rain'],
            522:['040-rain.png',    'Heavy Rain','Heavy intensity shower rain'],
            531:['010-rain-3.png',  '      Rain','Ragged shower rain'],
            600:['018-snowflake.png',   'Light Snow','Light snow'],
            601:['008-snow-1.png',  '      Snow','Snow'],
            602:['042-snow.png',    'Heavy Snow','Heavy snow'],
            611:['008-snow-1.png',  '     Sleet','Sleet'],
            612:['008-snow-1.png',  'Light Sleet','Light shower sleet'],
            613:['008-snow-1.png',  '      Snow','Shower sleet'],
            615:['018-snowflake.png',   '      Snow','Light rain and snow'],
            616:['042-snow.png',    'Rain & Snow','Rain and snow'],
            620:['018-snowflake.png',   'Light Snow','Light shower snow'],
            621:['008-snow-1.png',  'Shower Snow','Shower snow'],
            622:['042-snow.png',    'Heavy Snow','Heavy shower snow'],
            701:['015-clouds-3.png','      Mist','Mist'],
            711:['023-clouds-2.png','     Smoke','Smoke'],
            721:['015-clouds-3.png','      Haze','Haze'],
            731:['015-clouds-3.png','      Dust','Sand/dust whirls'],
            741:['023-clouds-2.png','      Fog','Fog'],
            751:['023-clouds-2.png','      Sand','Sand'],
            761:['023-clouds-2.png','      Dust','Dust'],
            762:['023-clouds-2.png','      Ash','Volcanic ash'],
            771:['022-wind.png',    '   Squalls','Squalls'],
            781:['013-tornado.png', '   Tornado','Tornado'],
            800:['050-sun.png',     ' Clear Sky','Clear sky'],
            801:['027-cloudy-1.png','Few Clouds','Few clouds: 11-25%'],
            802:['003-cloudy-4.png','    Cloudy','Scattered clouds: 25-50%'],
            803:['005-cloudy-3.png','    Cloudy','Broken clouds: 51-84%'],
            804:['049-clouds.png',  '  Overcast','Overcast clouds: 85-100%'],
        }
        # Time
        self.loadFonts()
        self.timeNow = datetime.now()
        self.count = 2
        self.getWeather()
        self.ab.run()
        if not self.OWMError:
            print(self.wid)
            print(self.currentTemp)
            print(self.weatherTable[self.wid][2])
        self.drawTime(doubleBuffer, count=self.count)
        self.drawABDay(doubleBuffer, self.ab.getDay(), count=self.count)
        self.drawWeather(doubleBuffer, count=self.count)
        return
    
    def restart(self, doubleBuffer):
        # Time
        now = datetime.now()
        self.timeNow = now
        self.ab.run()
        doubleBuffer.Clear()
        if self.weatherNow < datetime.now() or self.OWMError:
            self.OWMError = False
            self.getWeather()
        print(self.wid)
        print(self.currentTemp)
        print(self.weatherTable[self.wid][2])
        self.drawTime(doubleBuffer, count=self.count)
        self.drawABDay(doubleBuffer, self.ab.getDay(), count=self.count)
        self.drawWeather(doubleBuffer, count=self.count)
        return

    def run(self, doubleBuffer):
        updatedTime = False
        now = datetime.now()
        self.ab.run()
        if self.timeNow.minute != now.minute:
            print("Updating time in weatherAndTime")
            self.timeNow = now
            doubleBuffer.Clear()
            self.drawTime(doubleBuffer, count=self.count)
            self.drawABDay(doubleBuffer, self.ab.getDay(), count=self.count)
            updatedTime = True
        # Ensure that you've updated the time because that actually clears the screen.
        # Otherwise you MAY try to update the weather, but the screen wasn't cleared first.
        # We only clear the screen when the time needs to be updated.
        if self.weatherNow < datetime.now() or self.OWMError:
            self.OWMError = False
            self.getWeather()
            print(self.wid)
            print(self.currentTemp)
            print(self.weatherTable[self.wid][2])

        if updatedTime:
            self.drawWeather(doubleBuffer, count=self.count)
            return 1
        return 0
