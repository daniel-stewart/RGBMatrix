import time
from PIL import Image
from rgbmatrix import graphics
from matrixBaseClass import MatrixBaseClass

class MatrixScroller(MatrixBaseClass):
    def __init__(self, level):
        self.level = level % 2
    
    def initialize(self, width, height, double_buffer):
        if self.level == 0:
                self.font1 = graphics.Font()
                self.font2 = graphics.Font()
                self.font1.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/StarJedi-24.bdf")
                self.font2.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/RingbearerMedium-24.bdf")
                self.font3 = graphics.Font()
                self.font3.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/10x20.bdf")
                self.textColor = graphics.Color(255, 255, 0)
                self.pos = double_buffer.width
                self.index = 0
                self.my_text = [("All   we   have   to   decide   is   what   to   do   with   the   time   that   is   given   us.", self.font2),
                                ("There    is    some   good   in   this   world,   and    it's   worth   fighting   for.", self.font2),
                                ("i find your laCk of faith disturbing.", self.font1),
                                ("Do. or do not. There is no try.", self.font1),
                                ("Keep your options open.", self.font3)]
                print("Len of my_text:", len(self.my_text))
                self.length = len(self.my_text)
        elif self.level == 1:
                self.pos = 32
                self.index = 0
                self.images = ["/home/pi/Downloads/jessica.png", "/home/pi/Downloads/arabella.png", "/home/pi/Downloads/jacob.png", "/home/pi/Downloads/caleb.png"]
                self.image = Image.open(self.images[self.index]).convert('RGB')
                double_buffer.SetImage(self.image, 0, self.pos)
                self.length = len(self.images)
                print(self.image.height)
        
        
    def run(self, double_buffer):
        double_buffer.Clear()
        if self.level == 0:
                len = graphics.DrawText(double_buffer, self.my_text[self.index][1], self.pos, 25, self.textColor, self.my_text[self.index][0])
                self.pos -= 1
                if (self.pos + len < 0):
                    self.pos = double_buffer.width
                    self.index = (self.index + 1) % self.length

                time.sleep(0.02)
        elif self.level == 1:
                self.pos -= 1
                if (self.pos <=  -self.image.height):
                        # Finihsed showing image
                        self.pos = 32
                        self.index = (self.index + 1) % self.length
                        self.image = Image.open(self.images[self.index]).convert('RGB')
                double_buffer.SetImage(self.image, 0, self.pos)
                time.sleep(0.04)
                return True
        return True
