import time
import random
from PIL import Image
from rgbmatrix import graphics
from matrixBaseClass import MatrixBaseClass

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 128, 0)

class ImageSequence(MatrixBaseClass):
    def __init__(self, level):
        self.imageset = [("fireworks/fireworks%02d.png", 73), ("fire/fire%02d.png", 31), ("flag/flag%02d.png", 50), ("fireworks2/fireworks%02d.png", 30), ("water/water%02d.png", 30), ("rejoice/rejoice%02d.png", 1)]
        self.level = level % len(self.imageset)
        self.num = 0
        self.now = time.monotonic()
    
    def initialize(self, width, height, double_buffer):
        image = "/home/pi/icons/%s" %self.imageset[self.level][0]  %self.num
        image = Image.open(image).convert('RGB')
        double_buffer.SetImage(image, 0)
        self.now = time.monotonic()
        return
        
    def run(self, double_buffer):
        if (time.monotonic() - self.now) > 0.1:
            self.now = time.monotonic()
            self.num = (self.num + 1) % self.imageset[self.level][1]
            image = "/home/pi/icons/%s" %self.imageset[self.level][0] %self.num
            image = Image.open(image).convert('RGB')
            double_buffer.SetImage(image, 0)
            return True
        else:
            return False
