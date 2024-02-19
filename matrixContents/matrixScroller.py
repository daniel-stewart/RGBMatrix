import time
from PIL import Image
from rgbmatrix import graphics
from matrixBase import MatrixBase

# Add a secrets.py file to your project that has a dictionary
# called secrets with 'imagedir_prefix' equal to base path where all images are stored.
try:
    from secrets import secrets
except ImportError:
    print("imagedir_prefix NOT in secrets.py, please add them.")

YELLOW = (255, 255, 0)
BLUEWHITE = (128, 128, 255)
GREEN = (0, 255, 0)
REDISH = (255, 128, 128)
WHITE = (255, 255, 255)
ORANGE = (255, 128, 0)
CARROT = (255, 140, 25)
GOLDEN_BROWN = (153, 102, 0)

class MatrixScroller(MatrixBase):
    def __init__(self, level):
        self.level = level % 2
        self.bSecretFileExists = True
        self.imagedir_prefix = "/home/pi/ccs-rgb-matrix/images"
        self.fontDir_prefix = "/home/pi/rpi-rgb-led-matrix/fonts/"
    
    def initialize(self, width, height, double_buffer):
        self.imagedir_prefix = secrets['imagedir_prefix']
        self.fontdir_prefix = secrets['fontdir_prefix']
        if self.level == 0:
                self.font1 = graphics.Font()
                self.font2 = graphics.Font()
                self.font3 = graphics.Font()
                self.font4 = graphics.Font()
                #self.font1.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/extra/Mermaid-Bold-16.bdf")
                self.font1.LoadFont(self.fontdir_prefix + "extra/75dpi/timR14.bdf")
                self.font2.LoadFont(self.fontdir_prefix + "extra/RingbearerMedium-12.bdf")
                self.font3.LoadFont(self.fontdir_prefix + "10x20.bdf")
                self.font4.LoadFont(self.fontdir_prefix + "extra/75dpi/helvR12.bdf")
                self.textColor = graphics.Color(255, 255, 0)
                self.pos = double_buffer.width
                self.index = 0
                self.my_text = [("All   we   have   to   decide   is   what   to   do   with   the   time   that   is   given   us.", self.font2, YELLOW),
                                ("There    is    some   good   in   this   world,   and    it's   worth   fighting   for.", self.font2, YELLOW),
                                ("Made by the CCS Computer Club", self.font1, BLUEWHITE),
                                ("How is your day so far?", self.font1, YELLOW),
                                ("For God so loved the world, that He gave His only Son, that whoever believes in him should not perish but have eternal life", self.font3, GREEN),
                                ("Computers ... good stuff!", self.font1, BLUEWHITE),
                                ("Do what is right and good - Deut 6:18", self.font3, WHITE),
                                ("Good luck today!", self.font4, REDISH),
                                ("So... how about them Knights?", self.font1, ORANGE),
                                ("Hey guys!! It's me! Just saying hello...", self.font3, WHITE),
                                ("OK... so... anything exciting happening?", self.font4, YELLOW),
                                ("Do your homework?", self.font1, GOLDEN_BROWN)
                            ]
                print("Len of my_text:", len(self.my_text))
                self.length = len(self.my_text)
        elif self.level == 1:
                self.pos = double_buffer.height
                self.index = 0
                self.images = [self.imagedir_prefix + "/logo64.png"]
                self.image = Image.open(self.images[self.index]).convert('RGB')
                double_buffer.SetImage(self.image, 0, self.pos)
                self.length = len(self.images)
                print(self.image.height)
        
        
    def run(self, double_buffer):
        double_buffer.Clear()
        if self.level == 0:
                len = graphics.DrawText(double_buffer, self.my_text[self.index][1], self.pos, 25, graphics.Color(*self.my_text[self.index][2]), self.my_text[self.index][0])
                self.pos -= 1
                if (self.pos + len < 0):
                    self.pos = double_buffer.width
                    self.index = (self.index + 1) % self.length

                time.sleep(0.02)
        elif self.level == 1:
                self.pos -= 1
                if (self.pos <=  -self.image.height):
                        # Finished showing image
                        self.pos = double_buffer.height
                        self.index = (self.index + 1) % self.length
                        self.image = Image.open(self.images[self.index]).convert('RGB')
                double_buffer.SetImage(self.image, 0, self.pos)
                time.sleep(0.04)
        return 1
