from PIL import Image
from rgbmatrix import graphics
from matrixBase import MatrixBase
import random

RED = (255, 0, 0)
YELLOW = (255, 255, 0)
'''
Format for sprite sheets
String - Name/location of Sprite Sheet
A tuple of width, height of each icon
A tuple with row elements, each element is the number of icons in that row.
('/home/pi/ccs-rgb-matrix/icons/spriteSheets/Adventurer_Sprite_Sheet_v1.1.png', (32,32), (13, 8, 10, 10, 10, 6, 4, 7, 13, 8, 10, 10, 10, 6, 4, 7))

'''
class MatrixStayOnTarget(MatrixBase):
    def __init__(self, level):
        self.level = level
    
    def drawBox(self, x1, y1, x2, y2, x3, y3, x4, y4, doubleBuffer):
        graphics.DrawLine(doubleBuffer, x1, y1, x2, y2, graphics.Color(*YELLOW))
        graphics.DrawLine(doubleBuffer, x2, y2, x3, y3, graphics.Color(*YELLOW))
        graphics.DrawLine(doubleBuffer, x3, y3, x4, y4, graphics.Color(*YELLOW))
        return
    
    def drawSide(self, x0, y0, x1, y1, x2, y2, x3, y3, x4, y4, doubleBuffer):
        graphics.DrawLine(doubleBuffer, x0, y0, x1, y1, graphics.Color(*YELLOW))
        graphics.DrawLine(doubleBuffer, x0, y0, x2, y2, graphics.Color(*YELLOW))
        graphics.DrawLine(doubleBuffer, x0, y0, x3, y3, graphics.Color(*YELLOW))
        graphics.DrawLine(doubleBuffer, x0, y0, x4, y4, graphics.Color(*YELLOW))
        return

    def makeDisplay(self, doubleBuffer):
        self.drawSide(32,16, 0,0, 15,0, 0,31, 15,31, doubleBuffer)
        self.drawSide(32,16, 63,0, 48,0, 63,31, 48,31, doubleBuffer)
        graphics.DrawLine(doubleBuffer, 32, 16, 0, 15, graphics.Color(*YELLOW))
        graphics.DrawLine(doubleBuffer, 32, 16, 63, 15, graphics.Color(*YELLOW))
        return
    
    def initialize(self, width, height, doubleBuffer):
        self.width = width
        self.height = height
        self.makeDisplay(doubleBuffer)

    def run(self, doubleBuffer):
        return False