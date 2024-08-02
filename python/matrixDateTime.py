from datetime import datetime
from rgbmatrix import graphics
from matrixBaseClass import MatrixBaseClass

class MatrixDateTime(MatrixBaseClass):
    def __init__(self, level):
        pass
    
    def initialize(self, width, height, double_buffer):
        self.font = graphics.Font()
        self.font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/10x20.bdf")
        self.now = datetime.now()
        current_time = self.now.strftime("%-I:%M")
        offset = 13
        if self.now.hour%12 == 0 or self.now.hour%12 > 9:
            offset = 6
        length = graphics.DrawText(double_buffer, self.font, offset, 16, graphics.Color(0, 255, 0), current_time)
        current_date = self.now.strftime("%a %b %-d")
        self.font2 = graphics.Font()
        self.font2.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/6x13.bdf")
        length = graphics.DrawText(double_buffer, self.font2, 2, 28, graphics.Color(255, 255, 0), current_date)
        
    def run(self, double_buffer):
        now = datetime.now()
        if self.now.minute != now.minute:
            self.now = now
            double_buffer.Clear()
            current_time = now.strftime("%-I:%M")
            offset = 13
            if self.now.hour%12 == 0 or self.now.hour%12 > 9:
                offset = 6
            length = graphics.DrawText(double_buffer, self.font, offset, 16, graphics.Color(0, 255, 0), current_time)
            current_date = now.strftime("%a %b %-d")
            length = graphics.DrawText(double_buffer, self.font2, 2, 28, graphics.Color(255, 255, 0), current_date)
            return True
        return False
