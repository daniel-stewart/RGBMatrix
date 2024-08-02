from datetime import datetime
import random
from PIL import Image
from rgbmatrix import graphics
from matrixBaseClass import MatrixBaseClass

class MatrixOnAir(MatrixBaseClass):
    def __init__(self, level):
        self.level = level % 2
    
    def initialize(self, width, height, double_buffer):
        if self.level == 1:
                font = graphics.Font()
                font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/BellotaText-Bold-21.bdf")
                white = graphics.Color(255, 255, 255)
                red = graphics.Color(255, 0, 0)
                graphics.DrawLine(double_buffer, 0, 0, 0, 31, white)
                graphics.DrawLine(double_buffer, 1, 0, 1, 31, white)
                graphics.DrawLine(double_buffer, 63, 0, 63, 31, white)
                graphics.DrawLine(double_buffer, 62, 0, 62, 31, white)
                graphics.DrawLine(double_buffer, 2, 0, 10, 0, white)
                graphics.DrawLine(double_buffer, 2, 1, 10, 1, white)
                graphics.DrawLine(double_buffer, 2, 30, 10, 30, white)
                graphics.DrawLine(double_buffer, 2, 31, 10, 31, white)
                graphics.DrawLine(double_buffer, 53, 0, 61, 0, white)
                graphics.DrawLine(double_buffer, 53, 1, 61, 1, white)
                graphics.DrawLine(double_buffer, 53, 30, 61, 30, white)
                graphics.DrawLine(double_buffer, 53, 31, 61, 31, white)
                
                graphics.DrawLine(double_buffer, 3, 3, 12, 3, red)
                graphics.DrawLine(double_buffer, 4, 4, 12, 4, red)
                graphics.DrawLine(double_buffer, 5, 6, 12, 6, red)
                graphics.DrawLine(double_buffer, 6, 7, 12, 7, red)
                graphics.DrawLine(double_buffer, 7, 9, 12, 9, red)
                graphics.DrawLine(double_buffer, 8, 10, 12, 10, red)
                
                graphics.DrawLine(double_buffer, 51, 3, 60, 3, red)
                graphics.DrawLine(double_buffer, 51, 4, 59, 4, red)
                graphics.DrawLine(double_buffer, 51, 6, 58, 6, red)
                graphics.DrawLine(double_buffer, 51, 7, 57, 7, red)
                graphics.DrawLine(double_buffer, 51, 9, 56, 9, red)
                graphics.DrawLine(double_buffer, 51, 10, 55, 10, red)
                
                length = graphics.DrawText(double_buffer, font, 15, 16, graphics.Color(255, 0, 0), "ON")
                length = graphics.DrawText(double_buffer, font, 15, 32, graphics.Color(255, 0, 0), "AIR")
        else:
                white = graphics.Color(255, 255, 255)
                yellow = graphics.Color(255, 255, 0)
                orange = graphics.Color(255, 128, 0)
                blueish = graphics.Color(128, 128, 255)
                image = "/home/pi/rpi-rgb-led-matrix/bindings/python/samples/icons/voice32x32.png"
                image = Image.open(image).convert('RGB')
                double_buffer.SetImage(image, 0)
                graphics.DrawLine(double_buffer, 0,0, 0, 31, white)
                graphics.DrawLine(double_buffer, 1,0, 1, 31, white)
                graphics.DrawLine(double_buffer, 63, 0, 63, 31, white)
                graphics.DrawLine(double_buffer, 62, 0, 62, 31, white)
                font = graphics.Font()
                font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/9x18.bdf")
                length = graphics.DrawText(double_buffer, font, 33, 14, orange, "On")
                length = graphics.DrawText(double_buffer, font, 30, 30, orange, "Air")
        
    def run(self, double_buffer):
        return False
