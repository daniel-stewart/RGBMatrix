#!/usr/bin/env python3
import time
from samplebase import SampleBase
from PIL import Image
from rgbmatrix import graphics
from sprite import Sprite

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 128, 0)

class ImageShow(SampleBase):
    def __init__(self, *args, **kwargs):
        super(ImageShow, self).__init__(*args, **kwargs)
        self.parser.add_argument("-i", "--image", help="The image to display", default="../../../examples-api-use/runtext.ppm")
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")
        self.parser.add_argument("-l", "--level", help="How irritated the person is", default=0)
        

    def run(self):
        imageList = ['010-glasses.png', '009-thinking.png', '014-worried.png', '013-surprised.png', '021-angry.png', '005-angry.png']
        textList = [('All','good','Come on in'), ("Just",'doing','work stuff'), ('Have', 'an', 'issue'), ('Uh, oh', 'this', "isn't cool."), ('Very', 'very', 'frustrated'), ("Ahhhh!", 'Sooo', "Mad!!!")]
        textColor = [(GREEN, GREEN, GREEN), (GREEN, GREEN, YELLOW), (YELLOW, YELLOW, YELLOW), (ORANGE, YELLOW, ORANGE), (YELLOW, YELLOW, RED), (ORANGE, ORANGE, RED)]
        print(len(imageList))
        level = int(self.args.level) % len(imageList)
        image = "../../../../icons/matrix/3898417/24x24/" + imageList[level]
        #image = "/home/pi/Matrix_Portal_Eyes/eyes/cyclops/cyclops-eye.bmp"
        #if not 'image' in self.__dict__:
        #    self.image = Image.open(self.args.image).convert('RGB')
        self.image = Image.open(image).convert('RGB')
        #self.image.resize((self.matrix.width, self.matrix.height), Image.ANTIALIAS)

        double_buffer = self.matrix.CreateFrameCanvas()
        img_width, img_height = self.image.size
        print(img_width, img_height)
        print(self.matrix.width, self.matrix.height)

        # let's scroll
        xpos = 0
        double_buffer.SetImage(self.image, xpos)
        #double_buffer = self.matrix.SwapOnVSync(double_buffer)
        
        font = graphics.Font()
        font.LoadFont("../../../fonts/6x10.bdf")
        
        pos = 27
        my_text = self.args.text
        length = graphics.DrawText(double_buffer, font, pos, 10, graphics.Color(*textColor[level][0]), textList[level][0])
        length = graphics.DrawText(double_buffer, font, pos, 20, graphics.Color(*textColor[level][1]), textList[level][1])
        length = graphics.DrawText(double_buffer, font, pos if len(textList[level][2]) < 7 else 0, 32, graphics.Color(*textColor[level][2]), textList[level][2])
        
        double_buffer = self.matrix.SwapOnVSync(double_buffer)
        while True:
                pass
        '''
        #xpos += 1
        if (xpos > img_width):
        xpos = 0

        double_buffer.SetImage(self.image, -xpos)
        #double_buffer.SetImage(self.image, -xpos + img_width)

        double_buffer = self.matrix.SwapOnVSync(double_buffer)
        time.sleep(0.01)
        '''
        

# Main function
# e.g. call with
#  sudo ./image-show.py --chain=4
# if you have a chain of four
if __name__ == "__main__":
    image_show = ImageShow()
    #prite = Sprite(["--creature", "2"])
    
    if (not image_show.process()):
        image_show.print_help()
    '''
    if (not sprite.process()):
            sprite.print_help()
    '''
