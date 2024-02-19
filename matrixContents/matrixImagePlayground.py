import time
import random
from PIL import Image
from rgbmatrix import graphics
from matrixBase import MatrixBase
from datetime import datetime

# Add a secrets.py file to your project that has a dictionary
# called 'iconsdir_prefix' that holds all the icons you want to use.
try:
    from secrets import secrets
except ImportError:
    print("icondir_prefix not found in secrets.py, please add them.")
    bSecretFileExists = False

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 128, 0)
PINK = (255, 128, 128)
BLACK = (0, 0, 0)
DARKGREEN = (100, 110, 0)

'''
There will be a list that has:
        * An image list (from which one will be chosen randomly) with x and y coords
        * A series of (x,y) & text strings in  a tuple
            * (x, y, "Text String", font_path, color)
Example:
        [ [(3, 6, '/home/pi/icons/PixelArtIconPack/Helm03.png',), (16, 15, "Hello World", "/home/pi/rpi-rgb-led-matrix/fonts/6x10.bdf", GREEN)] ]
'''

class MatrixImagePlayground(MatrixBase):
    def __init__(self, level):
        self.origLevel = level
        if level == -1:
          self.level = random.randint(1,4)
        elif level == -3:
          self.level = random.randint(11,12)
          print('Got a -3, so turning that into ', self.level)
        else:
          self.level = level
        now = datetime.now()
        if self.level == -2:
          # What day is it?
          print("Today is", now.weekday())
          if now.weekday() == 0:
              self.level = 8
          elif now.weekday() == 1:
              self.level = 5
          elif now.weekday() == 2:
              self.level = 6
          elif now.weekday() == 3:
              self.level = 9
          elif now.weekday() == 4:
              self.level = 7
          else:
              self.level = random.randint(1,4)
    
    def initialize(self, width, height, double_buffer):
        self.iconPathPrefix = secrets['icondir_prefix'] # Original: '/home/pi/ccs-rgb-matrix/icons/'
        self.imagePathPrefix = secrets['imagedir_prefix']
        self.entries = [
            #0
            [ ((0,0,self.iconPathPrefix + 'CCSKnight.png'),),
              (33, 12, 'Go', '/home/pi/rpi-rgb-led-matrix/fonts/6x10.bdf', WHITE),
              (23, 28, 'Knights', '/home/pi/rpi-rgb-led-matrix/fonts/6x10.bdf', WHITE) ],
            #1
            [ ((0,0, self.iconPathPrefix + 'MVIconsPixelDailies/cupcake2.png'),),
              (23, 14, 'Need a', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', PINK),
              (3, 28, 'Cupcake?', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', YELLOW),],
            #2
            [ ((0,0, self.iconPathPrefix + 'MVIconsPixelDailies/lightbulb.png'),),
              (48, 10, 'I', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', YELLOW),
              (37, 21, 'have', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', YELLOW),
              (15, 32, 'an idea!', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', YELLOW),],
            #3
            [ ((37,0, self.iconPathPrefix + 'MVIconsPixelDailies/juice-carton.png'),),
              (0, 9, 'Orange', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', ORANGE),
              (9, 20, 'juice', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', WHITE),
              (0, 29, 'is good!', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', CYAN),],
            #4
            [ ((32,0, self.iconPathPrefix + 'MVIconsPixelDailies/onion-rings.png'),),
              (0, 9, 'Mmm...', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', BLUE),
              (0, 20, 'Onion', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', ORANGE),
              (0, 29, 'Rings!', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', PINK),],
            #5
            #[ ((16,0, self.iconPathPrefix + 'MVIconsPixelDailies/straw-drink.png'),),
            [ ((0,16, self.iconPathPrefix + 'TropicalSmoothie.png'), ),
              (11, 44, '', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', CYAN),
              (8, 60, '', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', PINK),],
            #6
            [ ((0,0, self.iconPathPrefix + 'icon_circle-cfa-logo.png'),),
              (0, 12, '', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', RED),
              (0, 28, '', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', RED),],
            #7
            [ ((16,3, self.iconPathPrefix + 'pizza32x32.png'),),
              (5, 57, 'Pizza!', '/home/pi/rpi-rgb-led-matrix/fonts/extra/75dpi/timR18.bdf', GREEN),
              (0, 28, '', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', WHITE),],
            #8
            [ ((0,16, self.iconPathPrefix + 'RedHotAndBlue.png'),),
              (10, 37, '', '/home/pi/rpi-rgb-led-matrix/fonts/extra/75dpi/timR14.bdf', WHITE),
              (10, 60, "", '/home/pi/rpi-rgb-led-matrix/fonts/extra/75dpi/timR14.bdf', WHITE),],
            #9
            [ ((0, 0, self.iconPathPrefix + 'Moes.png'),),
              (10, 47, '', '/home/pi/rpi-rgb-led-matrix/fonts/extra/75dpi/timR14.bdf', DARKGREEN),
              (0, 28, '', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', WHITE),],
            #10
            [ ((16, 0, self.iconPathPrefix + 'christmas_tree.png'),),
              (17, 45, 'Merry', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', RED),
              (6, 58, 'Christmas!', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', RED),],
            #11
            [ ((0, 0, self.iconPathPrefix + 'Blank.png'),),
              (11, 25, 'Welcome', '/home/pi/rpi-rgb-led-matrix/fonts/6x13.bdf', GREEN),
              (19, 42, 'Back!', '/home/pi/rpi-rgb-led-matrix/fonts/6x13.bdf', GREEN),],
            #12
            [ ((16, 0, self.iconPathPrefix + 'youreback.png'),),
              (15, 43, "You're", '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', WHITE),
              (15, 56, 'Back!', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', WHITE),],
            #13
            [ ((32, 0, self.iconPathPrefix + 'education.png'),),
              (0, 15, 'School', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', ORANGE),
              (0, 28, 'Again...', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', ORANGE),],
            #14
            [ ((16, 0, self.iconPathPrefix + 'thumbsUp.png'),),
              (14, 41, 'Have a', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', RED),
              (3, 54, 'Great Day!', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', RED),],
            #15
            [ ((16, 0, self.iconPathPrefix + 'checked.png'),),
              (6, 43, 'Ready for', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', RED),
              (8, 56, 'the Day?', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', RED),],
            #16
            [ ((16, 0, self.iconPathPrefix + 'valentines-day.png'),),
              (2, 43, "Valentine's", '/home/pi/rpi-rgb-led-matrix/fonts/extra/75dpi/timR10.bdf', RED),
              (20, 56, 'Day!', '/home/pi/rpi-rgb-led-matrix/fonts/extra/75dpi/timR10.bdf', RED),],
            #17
            [ ((0, 0, self.imagePathPrefix + '/logo64.png'),),
              (0, 0, '', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', WHITE),
              (0, 0, '', '/home/pi/rpi-rgb-led-matrix/fonts/helvR12.bdf', WHITE),],
        ]

        fontList = set({})
        for entry in self.entries:
            numEntries = len(entry)
            for i in range(1,numEntries):
                fontList.add(entry[i][3])
        self.fonts = dict({})
        for font in fontList:
            print(font)
            f = graphics.Font()
            f.LoadFont(font)
            self.fonts[font] = f
        print(self.fonts.values())
        self.level = self.level % len(self.entries)
        icon = random.randint(0, len(self.entries[self.level][0])-1)
        print(self.entries[self.level][0])
        baseImage = Image.new('RGBA', (64, 64), (0,0,0,0))
        image = Image.open(self.entries[self.level][0][icon][2])
        baseImage.alpha_composite(image, (0,0))
        baseImage = baseImage.convert('RGB')
        double_buffer.SetImage(baseImage, self.entries[self.level][0][icon][0], self.entries[self.level][0][icon][1])
        for i in range(1, len(self.entries[self.level])):
            entry = self.entries[self.level][i]
            print(entry[3])
            print(self.fonts[entry[3]])
            print(entry[0])
            graphics.DrawText(double_buffer, self.fonts[entry[3]], entry[0], entry[1], graphics.Color(*entry[4]), entry[2])
        return
    
    def restart(self, doubleBuffer):
        if self.origLevel == -1:
          self.level = random.randint(1,4)
        elif self.origLevel == -3:
          self.level = random.randint(11,12)
          print('Got a -3, so turning that into ', self.level)
        else:
          self.level = self.origLevel
        now = datetime.now()
        if self.level == -2:
        # What day is it?
          print("Today is", now.weekday())
          if now.weekday() == 0:
              self.level = 8
          elif now.weekday() == 1:
              self.level = 5
          elif now.weekday() == 2:
              self.level = 6
          elif now.weekday() == 3:
              self.level = 9
          elif now.weekday() == 4:
              self.level = 7
          else:
              self.level = random.randint(1,4)
        icon = random.randint(0, len(self.entries[self.level][0])-1)
        print(self.entries[self.level][0])
        baseImage = Image.new('RGBA', (64, 64), (0,0,0,0))
        image = Image.open(self.entries[self.level][0][icon][2])
        baseImage.alpha_composite(image, (0,0))
        baseImage = baseImage.convert('RGB')
        doubleBuffer.SetImage(baseImage, self.entries[self.level][0][icon][0], self.entries[self.level][0][icon][1])
        for i in range(1, len(self.entries[self.level])):
            entry = self.entries[self.level][i]
            print(entry[3])
            print(self.fonts[entry[3]])
            print(entry[0])
            graphics.DrawText(doubleBuffer, self.fonts[entry[3]], entry[0], entry[1], graphics.Color(*entry[4]), entry[2])
        return
        
    def run(self, double_buffer):
        return 0
