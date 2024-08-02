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

class ImageShow(MatrixBaseClass):
    def __init__(self, level):
        self.level = level
    
    def initialize(self, width, height, double_buffer):
        #imageList = ['010-glasses.png', '009-thinking.png', '014-worried.png', '013-surprised.png', '021-angry.png', '005-angry.png']
        #imageList = ['115-nerd.png', '053-nerd-5.png', '001-suspicious-1.png', '009-suspicious.png', '095-angry-1.png', '039-angry-3.png']
        #imageList = ['016-nerd.png', '029-robot.png', '014-thinking.png', '009-sad.png', '006-angry-1.png', '039-angry-2.png']
        #imageList = ['115-nerd.png', '053-nerd-5.png', 'microphone32.png', '009-suspicious.png', '095-angry-1.png', 'microphone32.png']
        imageList = [('115-nerd.png','028-nerd-8.png'), 
                     ('097-eyebrows.png', '029-robot.png'), 
                     ('001-suspicious-1.png',), 
                     ('009-suspicious.png','019-shocked-6.png','021-crazy-1.png','025-shocked-5.png'), 
                     ('095-angry-1.png', '039-angry-3.png', '033-angry-4.png'), 
                     ('039-angry-2.png', '006-angry-1.png')]
        textList = [('All','good,','Come on in'), ("Just",'doing','work stuff'), ("I am", 'fixing', 'an issue'), ('Uh, oh', 'this', "isn't cool."), ('Very', 'very', 'frustrated'), ("Ahhhh!", 'Sooo', "Mad!!!")]
        textColor = [(GREEN, GREEN, GREEN), (GREEN, GREEN, YELLOW), (YELLOW, YELLOW, YELLOW), (ORANGE, YELLOW, ORANGE), (YELLOW, YELLOW, RED), (ORANGE, ORANGE, RED)]
        #image = "../../../../icons/matrix/3898417/24x24/" + imageList[self.level]
        #image = "../../../../icons/743191-smileys/png/24x24/" + imageList[self.level]
        #image = "../../../../icons/983034-emoji/png/24x24/" + imageList[self.level]
        icon = random.randint(0,len(imageList[self.level])-1)
        image = "/home/pi/rpi-rgb-led-matrix/bindings/python/samples/icons/" + imageList[self.level][icon]
        image = Image.open(image).convert('RGB')
        double_buffer.SetImage(image, 0)
        
        font = graphics.Font()
        font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/6x10.bdf")
        
        pos = 27
        length = graphics.DrawText(double_buffer, font, pos, 10, graphics.Color(*textColor[self.level][0]), textList[self.level][0])
        length = graphics.DrawText(double_buffer, font, pos, 20, graphics.Color(*textColor[self.level][1]), textList[self.level][1])
        length = graphics.DrawText(double_buffer, font, pos if len(textList[self.level][2]) < 7 else 0, 32, graphics.Color(*textColor[self.level][2]), textList[self.level][2])
        
        return
        
    def run(self, double_buffer):
        return False
