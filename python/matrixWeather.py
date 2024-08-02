import random
from datetime import datetime
from datetime import timedelta
from PIL import Image
from rgbmatrix import graphics
from matrixBaseClass import MatrixBaseClass
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps

blue = graphics.Color(0, 0, 255)
cyan = graphics.Color(0, 255, 255)
blueWhite = graphics.Color(128, 128, 255)
darkBlue = graphics.Color(0, 0, 128)

class MatrixWeather(MatrixBaseClass):
    def __init__(self, level):
        self.level = level
        self.icon = ''
        self.temperture = {}
        self.status = 'Have a great day'

    def initialize(self, width, height, double_buffer):
        self.width = width
        self.height = height
        self.owm = OWM('680845da62c98556d84d1d2e8ad4e38b')
        self.mgr = self.owm.weather_manager()
        self.now = datetime.now() + timedelta(minutes=10)
        observation = self.mgr.weather_at_place('Cary,US')
        w = observation.weather
        icon_name = w.weather_icon_name
        status = w.detailed_status         # 'clouds'
        temperature = w.temperature('fahrenheit')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
        temp = round(temperature["temp"])
        print(temperature["temp"])

        icon = "/home/pi/icons/weather414925/414925-weather/png/32x32/" + str(w.weather_code) + ".png"
        print(icon)
        image = Image.open(icon).convert('RGB')
        double_buffer.SetImage(image, 0)
        font = graphics.Font()
        #font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/6x10.bdf")
        font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/7x13.bdf")
        pos = 40
        length = graphics.DrawText(double_buffer, font, pos, 20, blueWhite, str(temp)+"\u00B0")
        degrees = "/home/pi/icons/weather414925/414925-weather/png/32x32/degrees.png"
        #image = Image.open(degrees).convert('RGB')
        #double_buffer.SetImage(image, 40)
        
    
    def run(self, double_buffer):
        if self.now < datetime.now():
            
            observation = self.mgr.weather_at_place('Cary,US')
            w = observation.weather
            icon_name = w.weather_icon_name
            status = w.detailed_status         # 'clouds'
            temperature = w.temperature('fahrenheit')  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
            temp = round(temperature["temp"])
            print(temperature["temp"])

            icon = "/home/pi/icons/weather414925/414925-weather/png/32x32/" + str(w.weather_code) + ".png"
            print(icon)
            image = Image.open(icon).convert('RGB')
            double_buffer.Clear()
            double_buffer.SetImage(image, 0)
            font = graphics.Font()
            #font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/6x10.bdf")
            font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/7x13.bdf")
            pos = 40
            length = graphics.DrawText(double_buffer, font, pos, 20, blueWhite, str(temp)+"\u00B0")
            degrees = "/home/pi/icons/weather414925/414925-weather/png/32x32/degrees.png"
            self.now = datetime.now() + timedelta(minutes=10)
            return True
        return False
