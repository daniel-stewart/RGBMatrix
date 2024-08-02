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
PINK = (255, 128, 128)

'''
There will be a dict that has:
        * An image list (from which one will be chosen randomly) with x and y coords
        * A series of (x,y) & text strings in  a tuple
        * (x, y, "Text String", font_path, color)
Example:
        [ [(3, 6, '/home/pi/icons/PixelArtIconPack/Helm03.png',), (16, 15, "Hello World", "/home/pi/rpi-rgb-led-matrix/fonts/6x10.bdf", GREEN)] ]
'''

class MatrixImagePlayground(MatrixBaseClass):
    def __init__(self, level):
        self.level = level
    
    def initialize(self, width, height, double_buffer):
        entries = [
            [ ((-3,0,'/home/pi/icons/PixelArtIconPack/Helm03.png'),(-3,0,'/home/pi/icons/PixelArtIconPack/IronHelmet01.png'),(0,0,'/home/pi/icons/variables01_png/variables03spellbook_green.png')),
              (33, 12, 'Go', '/home/pi/rpi-rgb-led-matrix/fonts/6x10.bdf', WHITE),
              (23, 28, 'Knights', '/home/pi/rpi-rgb-led-matrix/fonts/6x10.bdf', WHITE) ],
            [ ((0,0,'/home/pi/icons/food/Ghostpixxells_pixelfood/16_burger_dish.png'),),
              (23, 28, 'Lunch?', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', GREEN),],
            [ ((0,0,'/home/pi/icons/MVIconsPixelDailies/cupcake2.png'),),
              (23, 14, 'Need a', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', PINK),
              (3, 28, 'Cupcake?', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', YELLOW),],
            [ ((0,0,'/home/pi/icons/MVIconsPixelDailies/lightbulb.png'),),
              (48, 10, 'I', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', YELLOW),
              (37, 21, 'have', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', YELLOW),
              (15, 32, 'an idea!', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', YELLOW),],
            [ ((37,0,'/home/pi/icons/MVIconsPixelDailies/juice-carton.png'),),
              (0, 9, 'Orange', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', ORANGE),
              (9, 20, 'juice', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', WHITE),
              (0, 29, 'is good!', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', CYAN),],
            [ ((32,0,'/home/pi/icons/MVIconsPixelDailies/onion-rings.png'),),
              (0, 9, 'Mmm...', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', BLUE),
              (0, 20, 'Onion', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', ORANGE),
              (0, 29, 'Rings!', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', PINK),],
            [ ((36,0,'/home/pi/icons/MVIconsPixelDailies/straw-drink.png'),),
              (0, 12, 'Tropical', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', CYAN),
              (0, 28, 'Smoothie!', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', PINK),],
        ]

        fontList = set({})
        for entry in entries:
            numEntries = len(entry)
            for i in range(1,numEntries):
                fontList.add(entry[i][3])
        fonts = dict({})
        for font in fontList:
            print(font)
            f = graphics.Font()
            f.LoadFont(font)
            fonts[font] = f
        print(fonts.values())
        self.level = self.level % len(entries)
        icon = random.randint(0, len(entries[self.level][0])-1)
        print(entries[self.level][0])
        image = Image.open(entries[self.level][0][icon][2]).convert('RGB')
        double_buffer.SetImage(image, entries[self.level][0][icon][0], entries[self.level][0][icon][1])
        for i in range(1, len(entries[self.level])):
            entry = entries[self.level][i]
            print(entry[3])
            print(fonts[entry[3]])
            print(entry[0])
            graphics.DrawText(double_buffer, fonts[entry[3]], entry[0], entry[1], graphics.Color(*entry[4]), entry[2])
        '''
        # Go through and make a font for each listed
        textList = [('Go','', 'Knights')]
        textColor = [(WHITE, WHITE, WHITE)]
        textPosition = [( (33, 12), (27, 20), (23, 28) )]
        self.level = self.level % len(imageList)
        print("Level", self.level)
        icon = random.randint(0,len(imageList[self.level])-1)
        image = imageList[self.level][icon]
        image = Image.open(image).convert('RGB')
        double_buffer.SetImage(image, -3)
        
        font = graphics.Font()
        font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/6x10.bdf")
        
        pos = 27
        length = graphics.DrawText(double_buffer, font, textPosition[self.level][0][0], textPosition[self.level][0][1], graphics.Color(*textColor[self.level][0]), textList[self.level][0])
        length = graphics.DrawText(double_buffer, font, textPosition[self.level][1][0], textPosition[self.level][1][1], graphics.Color(*textColor[self.level][1]), textList[self.level][1])
        length = graphics.DrawText(double_buffer, font, textPosition[self.level][2][0], textPosition[self.level][2][1], graphics.Color(*textColor[self.level][2]), textList[self.level][2])
        '''
        return
        
    def run(self, double_buffer):
        return False
