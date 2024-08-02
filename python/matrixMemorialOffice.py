from rgbmatrix import graphics
from matrixBaseClass import MatrixBaseClass

class MatrixMemorialOffice(MatrixBaseClass):
    def __init__(self, level):
        pass
    
    def initialize(self, width, height, double_buffer):
        self.font = graphics.Font()
        self.font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/6x10.bdf")
        text1 = "Harold"
        length = graphics.DrawText(double_buffer, self.font, 12, 7, graphics.Color(0, 255, 0), text1)
        length = graphics.DrawText(double_buffer, self.font, 10, 15, graphics.Color(0, 255, 0), "Stewart")
        self.font2 = graphics.Font()
        self.font2.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/6x10.bdf")
        text2 = "Memorial"
        length = graphics.DrawText(double_buffer, self.font2, 8, 23, graphics.Color(255, 255, 0), text2)
        length = graphics.DrawText(double_buffer, self.font2, 16, 31, graphics.Color(255, 255, 0), "Office")
        
    def run(self, double_buffer):
        return False
