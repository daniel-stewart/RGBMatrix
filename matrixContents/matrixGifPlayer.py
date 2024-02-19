from PIL import Image, ImageSequence, ImagePalette
from rgbmatrix import graphics
from matrixBase import MatrixBase
from datetime import datetime
import time
import random

# Add a secrets.py file to your project that has a dictionary
# called secrets with 'imagedir_prefix' equal to base path where all images are stored.
try:
    from secrets import secrets
except ImportError:
    print("icondir_prefix NOT in secrets.py, please add them.")

class MatrixGifPlayer(MatrixBase):
    def __init__(self, level):
        self.exitWhenDone = False
        self.level = level
    
    def initialize(self, width, height, doubleBuffer):
        self.iconPathPrefix = secrets['icondir_prefix'] # Original: '/home/pi/ccs-rgb-matrix/icons/'
        self.exit = False
        self.gifList = [
            (self.iconPathPrefix + '203_waterdrop.gif', True, (0,0)),
            (self.iconPathPrefix + '215_fallingcube.gif', True, (0,0)),
            (self.iconPathPrefix + '341_minion2.gif', True, (0,0)),
            (self.iconPathPrefix + '364_colortoroid.gif', False, (0,0)),
            (self.iconPathPrefix + '255_photon.gif', False, (0,0)),
            (self.iconPathPrefix + '412_bluecube_slide.gif', False, (0,0)),
            (self.iconPathPrefix + '342_spincircle.gif', False, (0,0)),
            (self.iconPathPrefix + '200_circlesmoke.gif', False, (0,0)),
            (self.iconPathPrefix + '284_comets.gif', False, (0,0)),
            (self.iconPathPrefix + '202.gif', True, (0,0)),
            (self.iconPathPrefix + '209.gif', False, (0,0)),
            (self.iconPathPrefix + '214.gif', False, (0,0)),
            (self.iconPathPrefix + '275.gif', False, (0,0)),
            (self.iconPathPrefix + '276.gif', False, (0,0)),
            (self.iconPathPrefix + '288.gif', False, (0,0)),
            (self.iconPathPrefix + '308.gif', False, (0,0)),
            (self.iconPathPrefix + 'Obiwan.gif', True, (150, 44)),
            (self.iconPathPrefix + 'obiwan2.gif', True, (90, 20)),
            (self.iconPathPrefix + 'itsatrap.gif', True, (27, 0)),
            (self.iconPathPrefix + 'princessleia.gif', True, (0,0))
        ]
        if type(self.level) is tuple:
            if self.level[0] == -1:
                r = random.randint(0, len(self.gifList)-1)
                self.gif = self.gifList[r][0]
                self.exitWhenDone = self.level[1]
                self.sourceCoord = self.gifList[r][2]
            else:
                self.gif = self.gifList[self.level[0]][0]
                self.exitWhenDone = self.level[1]
                self.sourceCoord = self.gifList[self.level[0]][2]
        else:
            if self.level == -1:
                r = random.randint(0, len(self.gifList) - 1)
                self.gif = self.gifList[r][0]
                self.exitWhenDone = self.gifList[r][1]
                self.sourceCoord = self.gifList[r][2]
            else:
                self.gif = self.gifList[self.level][0]
                self.exitWhenDone = self.gifList[self.level][1]
                self.sourceCoord = self.gifList[self.level][2]
        self.width = width
        self.height = height
        print('exit when done: ', self.exitWhenDone)
        self.gif = Image.open(self.gif)
        if self.gif.width != 32:
            baseImage = Image.new('RGBA', (doubleBuffer.width, doubleBuffer.height), (0,0,0,0))
            print("Number of frames: {}".format(self.gif.n_frames))
            baseImage.alpha_composite(self.gif.convert('RGBA'), (0,0), self.sourceCoord)
        else:
            if self.level > 8:
                baseImage = Image.new('RGBA', (doubleBuffer.width, doubleBuffer.height), (0,0,0,0))
            else:
                baseImage = Image.new('RGBA', (doubleBuffer.width, doubleBuffer.height), (255,255,255,0))
            print("Number of frames: {}".format(self.gif.n_frames))
            baseImage.alpha_composite(self.gif.convert('RGBA'), (16,0))
        self.now = time.monotonic()
        doubleBuffer.SetImage(baseImage.convert('RGB'))
        return
    
    def restart(self, doubleBuffer):
        self.exit = False
        if type(self.level) is tuple:
            if self.level[0] == -1:
                r = random.randint(0, len(self.gifList)-1)
                self.gif = self.gifList[r][0]
                self.exitWhenDone = self.level[1]
                self.sourceCoord = self.gifList[r][2]
            else:
                self.gif = self.gifList[self.level[0]][0]
                self.exitWhenDone = self.level[1]
                self.sourceCoord = self.gifList[self.level[0]][2]
        else:
            if self.level == -1:
                r = random.randint(0, len(self.gifList) - 1)
                self.gif = self.gifList[r][0]
                self.exitWhenDone = self.gifList[r][1]
                self.sourceCoord = self.gifList[r][2]
            else:
                self.gif = self.gifList[self.level][0]
                self.exitWhenDone = self.gifList[self.level][1]
                self.sourceCoord = self.gifList[self.level][2]
        self.gif = Image.open(self.gif)
        if self.gif.width != 32:
            baseImage = Image.new('RGBA', (doubleBuffer.width, doubleBuffer.height), (0,0,0,0))
            print("Number of frames: {}".format(self.gif.n_frames))
            baseImage.alpha_composite(self.gif.convert('RGBA'), (0,0), self.sourceCoord)
        else:
            if self.level > 8:
                baseImage = Image.new('RGBA', (doubleBuffer.width, doubleBuffer.height), (0,0,0,0))
            else:
                baseImage = Image.new('RGBA', (doubleBuffer.width, doubleBuffer.height), (255,255,255,0))
            print("Number of frames: {}".format(self.gif.n_frames))
            baseImage.alpha_composite(self.gif.convert('RGBA'), (16,0))
        self.now = time.monotonic()
        doubleBuffer.SetImage(baseImage.convert('RGB'))
        return
    
    def run(self, doubleBuffer):
        if time.monotonic() - self.now > 0.1:

            if self.exit == True:
                return 2
            
            if self.gif.tell() == self.gif.n_frames - 1:
                    self.gif.seek(0)
                    print("At end of gif animation")
                    if self.exitWhenDone:
                        print("   set exitWhenDone")
                        self.exit = True
            else:
                self.gif.seek(self.gif.tell() + 1)
            
            self.now = time.monotonic()
            if self.gif.width != 32:
                baseImage = Image.new('RGBA', (doubleBuffer.width, doubleBuffer.height), (0,0,0,0))
                baseImage.alpha_composite(self.gif.convert('RGBA'), (0,0), self.sourceCoord)
            else:
                if self.level > 8:
                    baseImage = Image.new('RGBA', (doubleBuffer.width, doubleBuffer.height), (0,0,0,0))
                else:
                    baseImage = Image.new('RGBA', (doubleBuffer.width, doubleBuffer.height), (255,255,255,0))
                baseImage.alpha_composite(self.gif.convert('RGBA'), (16,0))
            doubleBuffer.SetImage(baseImage.convert('RGB'))
            return 1
        else:
            return 0