from PIL import Image
from rgbmatrix import graphics
from matrixBaseClass import MatrixBaseClass
from datetime import datetime
import time

RED = (255, 0, 0)
'''
Format for sprite sheets
String - Name/location of Sprite Sheet
A tuple of width, height of each icon
A tuple with row elements, each element is the number of icons in that row.
('/home/pi/icons/Elthan/Adventurer_Sprite_Sheet_v1.1.png', (32,32), (13, 8, 10, 10, 10, 6, 4, 7, 13, 8, 10, 10, 10, 6, 4, 7))

'''
class MatrixSpriteViewer(MatrixBaseClass):
    def __init__(self, level):
        self.level = level

    def initialize(self, width, height, doubleBuffer):
        self.error = False
        self.spriteSheets = [
            ('/home/pi/icons/Elthan/Adventurer_Sprite_Sheet_v1.1.png', (32,32), (13, 8, 10, 10, 10, 6, 4, 7, 13, 8, 10, 10, 10, 6, 4, 7)),
            ('/home/pi/icons/Elthan/Banner.png', (32,32), (4, 4)),
            ('/home/pi/icons/Elthan/Torch.png', (8, 16), (10,)),
            ('/home/pi/icons/JunglePlatform/Decorations.png', (16, 16), (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1)),
            ('/home/pi/icons/Elthan/Destructible_Objects_Sprite_Sheet.png', (64, 64), (3, 7, 3, 7, 3 ,7, 3, 6, 3, 6, 3, 5)),
            ('/home/pi/icons/Elthan/Archaeologist_Sprite_Sheet.png', (32,32), (8, 8, 7, 6, 8, 4, 5))
        ]
        numberOfSpriteSheets = len(self.spriteSheets)
        self.level = self.level % numberOfSpriteSheets
        self.image = Image.open(self.spriteSheets[self.level][0]).convert('RGBA')
        self.set = 0
        self.index = 0
        self.width = width
        self.height = height
        baseImage = Image.new('RGBA', (width, height), (0,0,0,0))
        croppedImage = self.image.crop((self.index * self.spriteSheets[self.level][1][0], self.set * self.spriteSheets[self.level][1][1],
                              (self.index + 1) * self.spriteSheets[self.level][1][0],
                              (self.set+1) * self.spriteSheets[self.level][1][1]))
        background = Image.open('/home/pi/icons/Backgrounds/desert_65x36.png')
        baseImage.alpha_composite(background, (0,0))
        baseImage.alpha_composite(croppedImage,(0,0))
        baseImage = baseImage.convert('RGB')
        self.widthInNumberSprites = max(self.spriteSheets[self.level][2])
        print("Width in number of sprites", self.widthInNumberSprites)
        self.heightInNumberSprites = len(self.spriteSheets[self.level][2])
        print("Height in number of sprites", self.heightInNumberSprites)
        print("Image Height", self.image.height)
        print("Image width", self.image.width)
        if self.image.height != self.heightInNumberSprites * self.spriteSheets[self.level][1][1]:
            self.error = True
        if self.error:
            f = graphics.Font()
            f.LoadFont('/home/pi/rpi-rgb-led-matrix/fonts/10x20.bdf')
            red = graphics.Color(*RED)
            graphics.DrawText(doubleBuffer, f, 8,22, red, "Error")
            graphics.DrawLine(doubleBuffer, 0, 0, 0, 31, red)
            graphics.DrawLine(doubleBuffer, 1, 0, 1, 31, red)
            graphics.DrawLine(doubleBuffer, 63, 0, 63, 31, red)
            graphics.DrawLine(doubleBuffer, 62, 0, 62, 31, red)
            graphics.DrawLine(doubleBuffer, 2, 0, 61, 0, red)
            graphics.DrawLine(doubleBuffer, 2, 1, 61, 1, red)
            graphics.DrawLine(doubleBuffer, 2, 30, 61, 30, red)
            graphics.DrawLine(doubleBuffer, 2, 31, 61, 31, red)
            return

        doubleBuffer.SetImage(baseImage)
        self.now = time.monotonic()
        
    def run(self, doubleBuffer):
        if self.error:
            return False
        if (time.monotonic() - self.now) > 0.1:
            self.now = time.monotonic()
            self.index = (self.index + 1) % self.spriteSheets[self.level][2][self.set]
            if self.index == 0:
                self.set = (self.set + 1) % self.heightInNumberSprites
            baseImage = Image.new('RGBA', (self.width, self.height), (0,0,0,0))
            croppedImage = self.image.crop((self.index * self.spriteSheets[self.level][1][0], self.set * self.spriteSheets[self.level][1][1],
                                  (self.index + 1) * self.spriteSheets[self.level][1][0],
                                  (self.set+1) * self.spriteSheets[self.level][1][1]))
            #background = Image.open('/home/pi/icons/Backgrounds/Clouds_100x59.png')
            #baseImage.alpha_composite(background, (0,0), (20,20))
            #background = Image.open('/home/pi/icons/Backgrounds/Mountains_Loopable_56x31.png')
            #baseImage.alpha_composite(background, (0,1))
            baseImage.alpha_composite(croppedImage,(0,0))
            baseImage = baseImage.convert('RGB')
            self.widthInNumberSprites = max(self.spriteSheets[self.level][2])
            #print("Width in number of sprites", self.widthInNumberSprites)
            self.heightInNumberSprites = len(self.spriteSheets[self.level][2])
            #print("Height in number of sprites", self.heightInNumberSprites)
            #print("Image Height", self.image.height)
            #print("Image width", self.image.width)

            doubleBuffer.SetImage(baseImage)
            return True
        return False
