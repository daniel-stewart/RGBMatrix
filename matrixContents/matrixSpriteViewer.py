from PIL import Image
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

RED = (255, 0, 0)
'''
Format for sprite sheets
String - Name/location of Sprite Sheet
A tuple of width, height of each icon
A tuple with row elements, each element is the number of icons in that row.
A number indicating which row index should be used for the character sprite. Used to set self.set
('/home/pi/ccs-rgb-matrix/icons/spriteSheets/Adventurer_Sprite_Sheet_v1.1.png', (32,32), (13, 8, 10, 10, 10, 6, 4, 7, 13, 8, 10, 10, 10, 6, 4, 7), 1)

'''
class MatrixSpriteViewer(MatrixBase):
    def __init__(self, level):
        self.origLevel = level
        if level == -1:
            self.level = random.randint(0,6)
        else:
            self.level = level

    def setBackground(file, size, x, y, doubleBuffer):
        backgroundImage = Image.open(file).convert('RGBA')
        bkCroppedImage = backgroundImage.crop((self.index * self.spriteSheets[self.level][1][0], self.set * self.spriteSheets[self.level][1][1],
                        (self.index + 1) * self.spriteSheets[self.level][1][0],
                        (self.set+1) * self.spriteSheets[self.level][1][1]))
    
    def loadIndividualSpriteFromSpritesheet(self, imageFile, spriteSheetIndex, row, col, width, height):
        return imageFile.crop((row * self.spriteSheets[spriteSheetIndex][1][0], col * self.spriteSheets[spriteSheetIndex][1][1],
                        (row + width) * self.spriteSheets[spriteSheetIndex][1][0],
                        (col + height) * self.spriteSheets[spriteSheetIndex][1][1]))
    
    def loadImages(self):
        backgroundImage = Image.open(self.spriteSheets[7][0]).convert('RGBA')
        self.grassImage = self.loadIndividualSpriteFromSpritesheet(backgroundImage, 
                                                                    7, # The index into the self.spriteSheets
                                                                    1,  # Which column the sprite starts in, in terms of the base size of the the sprites, i.e., spriteSheets[1]
                                                                    1,  # Which row the sprite starts in, in terms of the base size of the sprites, i.e. spriteSheets[1]
                                                                    1,  # The width of the sprite, in terms of the size given in spriteSheets[1][0]
                                                                    1   # The height of the sprite, in terms of the size given in spriteSheets[1][1]
                                                                    )
        self.stumpImage = self.loadIndividualSpriteFromSpritesheet(backgroundImage, 
                                                                    7, # The index into the self.spriteSheets
                                                                    2,  # Which column the sprite starts in, in terms of the base size of the the sprites, i.e., spriteSheets[1]
                                                                    1,  # Which row the sprite starts in, in terms of the base size of the sprites, i.e. spriteSheets[1]
                                                                    1,  # The width of the sprite, in terms of the size given in spriteSheets[1][0]
                                                                    1   # The height of the sprite, in terms of the size given in spriteSheets[1][1]
                                                                    )
       
        self.altgrassImage = self.loadIndividualSpriteFromSpritesheet(backgroundImage, 
                                                                    7, # The index into the self.spriteSheets
                                                                    0,  # Which column the sprite starts in, in terms of the base size of the the sprites, i.e., spriteSheets[1]
                                                                    1,  # Which row the sprite starts in, in terms of the base size of the sprites, i.e. spriteSheets[1]
                                                                    1,  # The width of the sprite, in terms of the size given in spriteSheets[1][0]
                                                                    1   # The height of the sprite, in terms of the size given in spriteSheets[1][1]
                                                                    )
        
        self.mushroomImage = self.loadIndividualSpriteFromSpritesheet(backgroundImage, 
                                                                    7, # The index into the self.spriteSheets
                                                                    2,  # Which column the sprite starts in, in terms of the base size of the the sprites, i.e., spriteSheets[1]
                                                                    2,  # Which row the sprite starts in, in terms of the base size of the sprites, i.e. spriteSheets[1]
                                                                    1,  # The width of the sprite, in terms of the size given in spriteSheets[1][0]
                                                                    1   # The height of the sprite, in terms of the size given in spriteSheets[1][1]
                                                                    )

        self.flowerImage = self.loadIndividualSpriteFromSpritesheet(backgroundImage, 
                                                                    7, # The index into the self.spriteSheets
                                                                    0,  # Which column the sprite starts in, in terms of the base size of the the sprites, i.e., spriteSheets[1]
                                                                    0,  # Which row the sprite starts in, in terms of the base size of the sprites, i.e. spriteSheets[1]
                                                                    1,  # The width of the sprite, in terms of the size given in spriteSheets[1][0]
                                                                    1   # The height of the sprite, in terms of the size given in spriteSheets[1][1]
                                                                    )
        
        self.barrelImage = self.loadIndividualSpriteFromSpritesheet(backgroundImage, 
                                                                    7, # The index into the self.spriteSheets
                                                                    1,  # Which column the sprite starts in, in terms of the base size of the the sprites, i.e., spriteSheets[1]
                                                                    2,  # Which row the sprite starts in, in terms of the base size of the sprites, i.e. spriteSheets[1]
                                                                    1,  # The width of the sprite, in terms of the size given in spriteSheets[1][0]
                                                                    1   # The height of the sprite, in terms of the size given in spriteSheets[1][1]
                                                                    )

        self.bigmushroomImage = self.loadIndividualSpriteFromSpritesheet(backgroundImage, 
                                                                    7, # The index into the self.spriteSheets
                                                                    0,  # Which column the sprite starts in, in terms of the base size of the the sprites, i.e., spriteSheets[1]
                                                                    7,  # Which row the sprite starts in, in terms of the base size of the sprites, i.e. spriteSheets[1]
                                                                    2,  # The width of the sprite, in terms of the size given in spriteSheets[1][0]
                                                                    2   # The height of the sprite, in terms of the size given in spriteSheets[1][1]
                                                                    )
        
        self.emptyImage = self.loadIndividualSpriteFromSpritesheet(backgroundImage, 
                                                                    7, # The index into the self.spriteSheets
                                                                    3,  # Which column the sprite starts in, in terms of the base size of the the sprites, i.e., spriteSheets[1]
                                                                    5,  # Which row the sprite starts in, in terms of the base size of the sprites, i.e. spriteSheets[1]
                                                                    1,  # The width of the sprite, in terms of the size given in spriteSheets[1][0]
                                                                    1   # The height of the sprite, in terms of the size given in spriteSheets[1][1]
                                                                    )
        
        bigtreeLevel = 9
        bigtreeImage = Image.open(self.spriteSheets[bigtreeLevel][0]).convert('RGBA')
        self.bigtreeImage = self.loadIndividualSpriteFromSpritesheet(bigtreeImage, 
                                                                    9, # The index into the self.spriteSheets
                                                                    0,  # Which column the sprite starts in, in terms of the base size of the the sprites, i.e., spriteSheets[1]
                                                                    0,  # Which row the sprite starts in, in terms of the base size of the sprites, i.e. spriteSheets[1]
                                                                    4,  # The width of the sprite, in terms of the size given in spriteSheets[1][0]
                                                                    4   # The height of the sprite, in terms of the size given in spriteSheets[1][1]
                                                                    )
        
        self.bushImage = self.loadIndividualSpriteFromSpritesheet(bigtreeImage, 
                                                                    9, # The index into the self.spriteSheets
                                                                    4,  # Which column the sprite starts in, in terms of the base size of the the sprites, i.e., spriteSheets[1]
                                                                    3,  # Which row the sprite starts in, in terms of the base size of the sprites, i.e. spriteSheets[1]
                                                                    2,  # The width of the sprite, in terms of the size given in spriteSheets[1][0]
                                                                    1   # The height of the sprite, in terms of the size given in spriteSheets[1][1]
                                                                    )
        self.stoneImage = self.loadIndividualSpriteFromSpritesheet(bigtreeImage, 
                                                                    9, # The index into the self.spriteSheets
                                                                    6,  # Which column the sprite starts in, in terms of the base size of the the sprites, i.e., spriteSheets[1]
                                                                    3,  # Which row the sprite starts in, in terms of the base size of the sprites, i.e. spriteSheets[1]
                                                                    2,  # The width of the sprite, in terms of the size given in spriteSheets[1][0]
                                                                    1   # The height of the sprite, in terms of the size given in spriteSheets[1][1]
                                                                    )
        
        villageLevel = 10
        villageImage = Image.open(self.spriteSheets[villageLevel][0]).convert('RGBA')
        self.villageBush1 = self.loadIndividualSpriteFromSpritesheet(villageImage, 
                                                                    10, # The index into the self.spriteSheets
                                                                    18,  # Which column the sprite starts in, in terms of the base size of the the sprites, i.e., spriteSheets[1]
                                                                    2,  # Which row the sprite starts in, in terms of the base size of the sprites, i.e. spriteSheets[1]
                                                                    2,  # The width of the sprite, in terms of the size given in spriteSheets[1][0]
                                                                    2   # The height of the sprite, in terms of the size given in spriteSheets[1][1]
                                                                    )
        
        self.villageBush1 = self.loadIndividualSpriteFromSpritesheet(villageImage,
                                                                    10, # The index into the self.spriteSheets
                                                                    22, # Which column the sprite starts in, in terms of the base size of the the sprites, i.e., spriteSheets[1]
                                                                    36, # Which row the sprite starts in, in terms of the base size of the sprites, i.e. spriteSheets[1]
                                                                    4, # The width of the sprite, in terms of the size given in spriteSheets[1][0]
                                                                    2) # The height of the sprite, in terms of the size given in spriteSheets[1][1]
        
        self.villageSign1 = self.loadIndividualSpriteFromSpritesheet(villageImage,
                                                                    10,
                                                                    24,
                                                                    1,
                                                                    2,
                                                                    3)
        
        self.villagePumpkin1 = self.loadIndividualSpriteFromSpritesheet(villageImage,
                                                                    10,
                                                                    38,
                                                                    6,
                                                                    2,
                                                                    2)
        
        self.villageTree1 = self.loadIndividualSpriteFromSpritesheet(villageImage,
                                                                    10,
                                                                    43,
                                                                    29,
                                                                    8,
                                                                    9)

        self.villagePot1 = self.loadIndividualSpriteFromSpritesheet(villageImage,
                                                                    10,
                                                                    22,
                                                                    21,
                                                                    2,
                                                                    1)
        
        self.villageGrass1 = self.loadIndividualSpriteFromSpritesheet(villageImage,
                                                                    10,
                                                                    26,
                                                                    29,
                                                                    2,
                                                                    1)
        
        self.villageGrass2 = self.loadIndividualSpriteFromSpritesheet(villageImage,
                                                                    10,
                                                                    24,
                                                                    29,
                                                                    2,
                                                                    1)
        
        self.villageArcheryTarget = self.loadIndividualSpriteFromSpritesheet(villageImage,
                                                                    10,
                                                                    44,
                                                                    1,
                                                                    4,
                                                                    3)
        
        TreeImage = Image.open(self.spriteSheets[11][0]).convert('RGBA')
        self.treeTree1 = self.loadIndividualSpriteFromSpritesheet(TreeImage, 
                                                                    11, # The index into the self.spriteSheets
                                                                    2,  # Which column the sprite starts in, in terms of the base size of the the sprites, i.e., spriteSheets[1]
                                                                    1,  # Which row the sprite starts in, in terms of the base size of the sprites, i.e. spriteSheets[1]
                                                                    2,  # The width of the sprite, in terms of the size given in spriteSheets[1][0]
                                                                    2   # The height of the sprite, in terms of the size given in spriteSheets[1][1]
                                                                    )
        
        self.treeTree2 = self.loadIndividualSpriteFromSpritesheet(TreeImage, 
                                                                    11, # The index into the self.spriteSheets
                                                                    0,  # Which column the sprite starts in, in terms of the base size of the the sprites, i.e., spriteSheets[1]
                                                                    1,  # Which row the sprite starts in, in terms of the base size of the sprites, i.e. spriteSheets[1]
                                                                    2,  # The width of the sprite, in terms of the size given in spriteSheets[1][0]
                                                                    2   # The height of the sprite, in terms of the size given in spriteSheets[1][1]
                                                                    )

        SunnylandPropsImage = Image.open(self.spriteSheets[12][0]).convert('RGBA')
        self.sunnylandMushroom = self.loadIndividualSpriteFromSpritesheet(SunnylandPropsImage, 
                                                                    12, # The index into the self.spriteSheets
                                                                    6,  # Which column the sprite starts in, in terms of the base size of the the sprites, i.e., spriteSheets[1]
                                                                    7,  # Which row the sprite starts in, in terms of the base size of the sprites, i.e. spriteSheets[1]
                                                                    1,  # The width of the sprite, in terms of the size given in spriteSheets[1][0]
                                                                    1   # The height of the sprite, in terms of the size given in spriteSheets[1][1]
                                                                    )
        
        self.sunnylandTree = self.loadIndividualSpriteFromSpritesheet(SunnylandPropsImage, 
                                                                    12, # The index into the self.spriteSheets
                                                                    7,  # Which column the sprite starts in, in terms of the base size of the the sprites, i.e., spriteSheets[1]
                                                                    2,  # Which row the sprite starts in, in terms of the base size of the sprites, i.e. spriteSheets[1]
                                                                    8,  # The width of the sprite, in terms of the size given in spriteSheets[1][0]
                                                                    6   # The height of the sprite, in terms of the size given in spriteSheets[1][1]
                                                                    )
        
        self.sunnylandSkull = self.loadIndividualSpriteFromSpritesheet(SunnylandPropsImage, 
                                                                    12, # The index into the self.spriteSheets
                                                                    11,  # Which column the sprite starts in, in terms of the base size of the the sprites, i.e., spriteSheets[1]
                                                                    12,  # Which row the sprite starts in, in terms of the base size of the sprites, i.e. spriteSheets[1]
                                                                    1,  # The width of the sprite, in terms of the size given in spriteSheets[1][0]
                                                                    1   # The height of the sprite, in terms of the size given in spriteSheets[1][1]
                                                                    )


        # Each asset group should have the same size asset
        self.layer0Assets = [
            self.grassImage,
            self.altgrassImage,
        ]
        self.layer1Assets = [
            self.villageGrass1,
            self.villageGrass2,
            self.stumpImage,
            self.barrelImage,
            self.emptyImage,
            self.mushroomImage,
            self.emptyImage,
            self.emptyImage,
            self.sunnylandMushroom,
            self.sunnylandSkull,
        ]
        self.layer2Assets = [
            #self.bushImage,
            #self.villageBush1,
            #self.stoneImage,
            #self.villageRock1,
            self.villageSign1,
            self.villagePumpkin1,
            self.villageTree1,
            self.villagePot1,
            self.villageArcheryTarget,
        ]
        self.layer3Assets = [
            self.bigtreeImage,
            self.treeTree1,
            self.treeTree2,
            self.sunnylandTree,
            #self.bigmushroomImage
        ]

    def initialize(self, width, height, doubleBuffer):
        self.iconPathPrefix = secrets['icondir_prefix'] # Original: '/home/pi/ccs-rgb-matrix/icons/'
        self.error = False
        self.spriteSheets = [
            (self.iconPathPrefix + 'spriteSheets/Adventurer_Sprite_Sheet_v1.1.png', (32,32), (13, 8, 10, 10, 10, 6, 4, 7, 13, 8, 10, 10, 10, 6, 4, 7), 1),
            (self.iconPathPrefix + 'spriteSheets/Archaeologist_Sprite_Sheet.png', (64,32), (8, 8, 7, 6, 8, 4, 5), 1),
            (self.iconPathPrefix + 'spriteSheets/LightBanditRev.png', (48, 48), (8,8,8,8,8), 1),
            (self.iconPathPrefix + 'spriteSheets/Dwarf_Sprite_Sheet.png', (64,32), (5, 8, 7, 6, 2, 5, 4, 7), 1),
            (self.iconPathPrefix + 'spriteSheets/FoxSpriteSheet.png', (32, 32), (5, 14, 8, 11, 5, 6, 7), 2),
            (self.iconPathPrefix + 'spriteSheets/Run-Sheet.png', (80, 64), (8,), 0),
            (self.iconPathPrefix + 'spriteSheets/adventurer-run3-sword-Sheet.png', (50,37), (6,), 0),
            (self.iconPathPrefix + 'spriteSheets/Decorations.png', (16, 16), (4, 4, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1), 1),
            (self.iconPathPrefix + 'spriteSheets/Destructible_Objects_Sprite_Sheet.png', (64, 64), (3, 7, 3, 7, 3 ,7, 3, 6, 3, 6, 3, 5), 1),
            (self.iconPathPrefix + 'spriteSheets/FreeCuteTileset/Decors.png', (28,28), (2, 2, 2, 4), 1),
            (self.iconPathPrefix + 'spriteSheets/TX_Village_Props.png', (16, 16), (1,), 1),       # The last two entires don't really matter because it isn't a running sprite. Just props for us to grab.
            (self.iconPathPrefix + 'spriteSheets/Trees.png', (64,64), (1,), 1),
            (self.iconPathPrefix + 'spriteSheets/SunnylandProps.png', (16, 16), (1,), 1),
        ]
        numberOfSpriteSheets = len(self.spriteSheets)
        self.loadImages()
        self.Layer0 = [
                        [self.layer0Assets[random.randint(0, len(self.layer0Assets)-1)], 0],
                        [self.layer0Assets[random.randint(0, len(self.layer0Assets)-1)], 16],
                        [self.layer0Assets[random.randint(0, len(self.layer0Assets)-1)], 32],
                        [self.layer0Assets[random.randint(0, len(self.layer0Assets)-1)], 48],
                        [self.layer0Assets[random.randint(0, len(self.layer0Assets)-1)], 64],
                      ]
        self.Layer1 = [
                       [self.layer1Assets[random.randint(0, len(self.layer1Assets)-1)], 8],
#                       [self.layer1Assets[random.randint(0, len(self.layer1Assets)-1)], 16],
                       [self.layer1Assets[random.randint(0, len(self.layer1Assets)-1)], 40],
#                       [self.layer1Assets[random.randint(0, len(self.layer1Assets)-1)], 48],
                       [self.layer1Assets[random.randint(0, len(self.layer1Assets)-1)], 64],
                      ]
        self.Layer2 = [
                       [self.layer2Assets[random.randint(0,len(self.layer2Assets)-1)], 0],
                       [self.layer2Assets[random.randint(0,len(self.layer2Assets)-1)], doubleBuffer.width],
#                       [self.layer2Assets[random.randint(0,len(self.layer2Assets)-1)], -1],
#                       [self.layer2Assets[random.randint(0,len(self.layer2Assets)-1)], -1],
#                       [self.layer2Assets[random.randint(0,len(self.layer2Assets)-1)], -1],
                      ]
        self.Layer3 = [
                       [self.layer3Assets[random.randint(0,len(self.layer3Assets)-1)], 0],
                       [self.layer3Assets[random.randint(0,len(self.layer3Assets)-1)], doubleBuffer.width],
                       #self.layer3Assets[random.randint(0,len(self.layer3Assets)-1)],
                      ]
        self.level = self.level % numberOfSpriteSheets
        self.image = Image.open(self.spriteSheets[self.level][0]).convert('RGBA')
        self.set = self.spriteSheets[self.level][3]
        self.index = 0
        self.width = width
        self.height = height
        self.stop = False
        self.x = -self.spriteSheets[self.level][1][0]   # This puts the character off the screen at the beginning.
        self.y = doubleBuffer.height - self.spriteSheets[self.level][1][1]  # The self.y value is how far down we should start drawing the sprite. Which is the difference between the canvas height and the sprite height.
        print('y is ', self.y, 'doubleBuffer.width:', doubleBuffer.width, 'doubleBuffer.height:', doubleBuffer.height)
        self.loadImages()
        baseImage = Image.new('RGBA', (doubleBuffer.width, doubleBuffer.height), (0,0,0,0))
        croppedImage = self.image.crop((self.index * self.spriteSheets[self.level][1][0], self.set * self.spriteSheets[self.level][1][1],
                              (self.index + 1) * self.spriteSheets[self.level][1][0],
                              (self.set+1) * self.spriteSheets[self.level][1][1]))
        background = Image.open(self.iconPathPrefix + 'spriteSheets/FreeCuteTileset/BG1.png')
        baseImage.alpha_composite(background, (0,0))
        #background = Image.new('RGBA', (width,height), (0, 255, 255, 255))
        #baseImage.alpha_composite(background, (0,0))

        # Layer 3, Far background objects
        for i in range(len(self.Layer3)):
            if doubleBuffer.height < self.Layer3[0][0].height:
                quant = int(self.Layer3[0][0].height / doubleBuffer.height)
                baseImage.alpha_composite(self.Layer3[0][0], (self.Layer3[0][1],0), (0, self.Layer3[0][0].height - doubleBuffer.height))
            else:
                baseImage.alpha_composite(self.Layer3[0][0], (self.Layer3[0][1], doubleBuffer.height-self.Layer3[0][0].height), (0, 0))

        #baseImage.alpha_composite(self.layer3[2], (112,0), (abs(self.layer3X), 24))
        # Layer 1, mid-mid-background objects
        # Put first object at (0,0) in doubleBuffer
        if doubleBuffer.height < self.Layer1[0][0].height:
            quant = int(self.Layer1[0][0].height / doubleBuffer.height)
            baseImage.alpha_composite(self.Layer1[0][0], (self.Layer1[0][1],0), (0, self.Layer1[0][0].height - doubleBuffer.height))
        else:
            baseImage.alpha_composite(self.Layer1[0][0], (self.Layer1[0][1], doubleBuffer.height-self.Layer1[0][0].height), (0, 0))

        # Layer 2, mid-background objects
        for i in range(len(self.Layer2)):
            if doubleBuffer.height < self.Layer2[0][0].height:
                quant = int(self.Layer2[0][0].height / doubleBuffer.height)
                baseImage.alpha_composite(self.Layer2[0][0], (self.Layer2[0][1],0), (0, self.Layer2[0][0].height - doubleBuffer.height))
            else:
                baseImage.alpha_composite(self.Layer2[0][0], (self.Layer2[0][1], doubleBuffer.height-self.Layer2[0][0].height), (0, 0))

        # Layer 0, Background objects
        # Layer 2, mid-background objects
        for i in range(len(self.Layer0)):
            if doubleBuffer.height < self.Layer0[0][0].height:
                quant = int(self.Layer0[0][0].height / doubleBuffer.height)
                baseImage.alpha_composite(self.Layer0[0][0], (self.Layer0[0][1],0), (0, self.Layer0[0][0].height - doubleBuffer.height))
            else:
                baseImage.alpha_composite(self.Layer0[0][0], (self.Layer0[0][1], doubleBuffer.height-self.Layer0[0][0].height), (0, 0))

        if self.x < 0:
            baseImage.alpha_composite(croppedImage, (0,self.y),(abs(self.x), 0))
        else:
            baseImage.alpha_composite(croppedImage,(self.x,self.y))
        baseImage = baseImage.convert('RGB')
        self.widthInNumberSprites = max(self.spriteSheets[self.level][2])
        print("Width in number of sprites", self.widthInNumberSprites)
        self.heightInNumberSprites = len(self.spriteSheets[self.level][2])
        print("Height in number of sprites", self.heightInNumberSprites)
        print("Image Height", self.image.height)
        print("Image width", self.image.width)
        if self.image.height != self.heightInNumberSprites * self.spriteSheets[self.level][1][1]:
            #self.error = True
            pass
        if self.image.width != self.widthInNumberSprites * self.spriteSheets[self.level][1][0]:
            #self.error = True
            pass
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
        return
    
    def restart(self, doubleBuffer):
        if self.origLevel == -1:
            self.level = random.randint(0,6)
            self.set = self.spriteSheets[self.level][3]
            self.image = Image.open(self.spriteSheets[self.level][0]).convert('RGBA')
            self.x = -self.spriteSheets[self.level][1][0]   # This puts the character off the screen at the beginning.
            self.y = doubleBuffer.height - self.spriteSheets[self.level][1][1]
        
    def run(self, doubleBuffer):
        if self.error:
            return 0
        if (time.monotonic() - self.now) > 0.1:
            self.now = time.monotonic()
            self.index = (self.index + 1) % self.spriteSheets[self.level][2][self.set]      # This will run through each sprite in the set of sprites for a run.
            #if self.index == 0:
            #    self.set = (self.set + 1) % self.heightInNumberSprites
            baseImage = Image.new('RGBA', (doubleBuffer.width, doubleBuffer.height), (0,0,0,0))
            croppedImage = self.loadIndividualSpriteFromSpritesheet(self.image, 
                                                                self.level,  # The index into the self.spriteSheets
                                                                self.index,  # Which column the sprite starts in, in terms of the base size of the the sprites, i.e., spriteSheets[1]
                                                                self.set,  # Which row the sprite starts in, in terms of the base size of the sprites, i.e. spriteSheets[1]
                                                                1,  # The width of the sprite, in terms of the size given in spriteSheets[1][0]
                                                                1   # The height of the sprite, in terms of the size given in spriteSheets[1][1]
                                                                )
            #croppedImage = self.image.crop((self.index * self.spriteSheets[self.level][1][0], self.set * self.spriteSheets[self.level][1][1],
            #                      (self.index + 1) * self.spriteSheets[self.level][1][0],
            #                      (self.set+1) * self.spriteSheets[self.level][1][1]))
            #background = Image.open('/home/pi/icons/Backgrounds/Clouds_100x59.png')
            background = Image.open(self.iconPathPrefix + 'spriteSheets/FreeCuteTileset/BG1.png')
            #baseImage.alpha_composite(background, (0,0), (20,20))
            #background = Image.open('/home/pi/icons/Backgrounds/Mountains_Loopable_56x31.png')
            #background = Image.new('RGBA', (self.width,self.height), (0, 255, 255, 255))
            baseImage.alpha_composite(background, (0,0))
            # Layer 3, Far background objects
            for i in range(len(self.Layer3)):  # We are only going to do 2 entries from this layer
                if doubleBuffer.height < self.Layer3[i][0].height:
                    quant = int(self.Layer3[i][0].height / doubleBuffer.height)
                    if self.Layer3[i][1] < 0:   # Now we need to simply start further in on the source image when copy...
                        baseImage.alpha_composite(self.Layer3[i][0], (0, 0), (-self.Layer3[i][1], self.Layer3[i][0].height - doubleBuffer.height))
                    else:
                        baseImage.alpha_composite(self.Layer3[i][0], (self.Layer3[i][1],0), (0, self.Layer3[i][0].height - doubleBuffer.height))
                else:
                    if self.Layer3[i][1] < 0:   # Now we need to simply start further in on the source image when copy...
                        baseImage.alpha_composite(self.Layer3[i][0], (0, doubleBuffer.width-self.Layer3[i][0].height), (-self.Layer3[i][1], 0))
                    else:
                        baseImage.alpha_composite(self.Layer3[i][0], (self.Layer3[i][1],doubleBuffer.width-self.Layer3[i][0].height), (0, 0))

            # Layer 2, mid-background objects
            for i in range(len(self.Layer2)):  # We are going to do all entries from this layer
                if doubleBuffer.height < self.Layer2[i][0].height:
                    quant = int(self.Layer2[i][0].height / doubleBuffer.height)
                    if self.Layer2[i][1] < 0:   # Now we need to simply start further in on the source image when copy...
                        baseImage.alpha_composite(self.Layer2[i][0], (0, 0), (-self.Layer2[i][1], self.Layer2[i][0].height - doubleBuffer.height))
                    else:
                        baseImage.alpha_composite(self.Layer2[i][0], (self.Layer2[i][1],0), (0, self.Layer2[i][0].height - doubleBuffer.height))
                else:
                    if self.Layer2[i][1] < 0:   # Now we need to simply start further in on the source image when copy...
                        baseImage.alpha_composite(self.Layer2[i][0], (0, doubleBuffer.width-self.Layer2[i][0].height), (-self.Layer2[i][1], 0))
                    else:
                        baseImage.alpha_composite(self.Layer2[i][0], (self.Layer2[i][1],doubleBuffer.width-self.Layer2[i][0].height), (0, 0))

            # Layer 1, background objects
            for i in range(len(self.Layer1)):  # We are only going to do 2 entries from this layer
                if doubleBuffer.height < self.Layer1[i][0].height:
                    quant = int(self.Layer1[i][0].height / doubleBuffer.height)
                    if self.Layer1[i][1] < 0:   # Now we need to simply start further in on the source image when copy...
                        baseImage.alpha_composite(self.Layer1[i][0], (0, 0), (-self.Layer1[i][1], self.Layer1[i][0].height - doubleBuffer.height))
                    else:
                        baseImage.alpha_composite(self.Layer1[i][0], (self.Layer1[i][1],0), (0, self.Layer1[i][0].height - doubleBuffer.height))
                else:
                    if self.Layer1[i][1] < 0:   # Now we need to simply start further in on the source image when copy...
                        baseImage.alpha_composite(self.Layer1[i][0], (0, doubleBuffer.width-self.Layer1[i][0].height), (-self.Layer1[i][1], 0))
                    else:
                        baseImage.alpha_composite(self.Layer1[i][0], (self.Layer1[i][1],doubleBuffer.width-self.Layer1[i][0].height), (0, 0))
            
            # Layer 0, background objects
            for i in range(len(self.Layer0)):  # We are going to do all entries from this layer
                if doubleBuffer.height < self.Layer0[i][0].height:
                    quant = int(self.Layer0[i][0].height / doubleBuffer.height)
                    if self.Layer0[i][1] < 0:   # Now we need to simply start further in on the source image when copy...
                        baseImage.alpha_composite(self.Layer0[i][0], (0, 0), (-self.Layer0[i][1], self.Layer0[i][0].height - doubleBuffer.height))
                    else:
                        baseImage.alpha_composite(self.Layer0[i][0], (self.Layer0[i][1],0), (0, self.Layer0[i][0].height - doubleBuffer.height))
                else:
                    if self.Layer0[i][1] < 0:   # Now we need to simply start further in on the source image when copy...
                        baseImage.alpha_composite(self.Layer0[i][0], (0, doubleBuffer.width-self.Layer0[i][0].height), (-self.Layer0[i][1], 0))
                    else:
                        baseImage.alpha_composite(self.Layer0[i][0], (self.Layer0[i][1],doubleBuffer.width-self.Layer0[i][0].height), (0, 0))
            
            if self.x < 0:
                baseImage.alpha_composite(croppedImage, (0,self.y),(abs(self.x), 0))
            else:
                baseImage.alpha_composite(croppedImage,(self.x,self.y))
            if (self.spriteSheets[self.level][1][0] / 2 + self.x) < 32:
                self.x = self.x + 4
            else:
                if not self.stop:
                    entryToPop = []
                    for index in range(len(self.Layer0)):
                        self.Layer0[index][1] -= 4
                        if self.Layer0[index][1] < -self.Layer0[index][0].width:
                            entryToPop.append(index)
                    for i in entryToPop:
                        self.Layer0.pop(i)
                        self.Layer0.insert(i, [self.layer0Assets[random.randint(0, len(self.layer0Assets)-1)], doubleBuffer.width])

                    entryToPop = []
                    # Note that the entire list is used, even though we only really composite 2 images above.
                    for index in range(len(self.Layer1)):
                        self.Layer1[index][1] -= 3
                        if self.Layer1[index][1] < -self.Layer1[index][0].width:
                            entryToPop.append(index)
                    for i in entryToPop:
                        self.Layer1.pop(i)
                        self.Layer1.insert(i, [self.layer1Assets[random.randint(0, len(self.layer1Assets)-1)], doubleBuffer.width])

                    entryToPop = []
                    for index in range(len(self.Layer2)):
                        self.Layer2[index][1] -= 2
                        if self.Layer2[index][1] < -self.Layer2[index][0].width:
                            entryToPop.append(index)
                    for i in entryToPop:
                        self.Layer2.pop(i)
                        self.Layer2.insert(i, [self.layer2Assets[random.randint(0, len(self.layer2Assets)-1)], doubleBuffer.width])

                    entryToPop = []
                    for index in range(len(self.Layer3)):
                        self.Layer3[index][1] -= 1
                        if self.Layer3[index][1] < -self.Layer3[index][0].width:
                            entryToPop.append(index)
                    for i in entryToPop:
                        self.Layer3.pop(i)
                        self.Layer3.insert(i, [self.layer3Assets[random.randint(0, len(self.layer3Assets)-1)], doubleBuffer.width])


            if self.x >= 64:
                self.x = -self.spriteSheets[self.level][1][0]
            baseImage = baseImage.convert('RGB')
            self.widthInNumberSprites = max(self.spriteSheets[self.level][2])
            #print("Width in number of sprites", self.widthInNumberSprites)
            self.heightInNumberSprites = len(self.spriteSheets[self.level][2])
            #print("Height in number of sprites", self.heightInNumberSprites)
            #print("Image Height", self.image.height)
            #print("Image width", self.image.width)
            doubleBuffer.SetImage(baseImage)
            return 1
        return 0
