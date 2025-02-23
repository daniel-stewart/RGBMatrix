import argparse
import time
import sys
import os
import random
import socket
from datetime import datetime, timedelta, time, date

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/..'))
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics
from matrixBase import MatrixBase
from matrixDateTime import MatrixDateTime
from matrixAB import MatrixAB
from matrixWeather import MatrixWeather
from matrixSprite import MatrixSprite
from matrixImagePlayground import MatrixImagePlayground
from matrixScroller import MatrixScroller
from matrixSpriteViewer import MatrixSpriteViewer
from matrixGifPlayer import MatrixGifPlayer
from matrixStayOnTarget import MatrixStayOnTarget
from matrixWeatherAndTime import MatrixWeatherAndTime

class MatrixDriver(object):
    def __init__(self, *args, **kwargs):
        self.parser = argparse.ArgumentParser()

        self.parser.add_argument("-r", "--led-rows", action="store", help="Display rows. 16 for 16x32, 32 for 32x32. Default: 32", default=32, type=int)
        self.parser.add_argument("--led-cols", action="store", help="Panel columns. Typically 32 or 64. (Default: 32)", default=32, type=int)
        self.parser.add_argument("-c", "--led-chain", action="store", help="Daisy-chained boards. Default: 1.", default=1, type=int)
        self.parser.add_argument("-P", "--led-parallel", action="store", help="For Plus-models or RPi2: parallel chains. 1..3. Default: 1", default=1, type=int)
        self.parser.add_argument("-p", "--led-pwm-bits", action="store", help="Bits used for PWM. Something between 1..11. Default: 11", default=11, type=int)
        self.parser.add_argument("-b", "--led-brightness", action="store", help="Sets brightness level. Default: 100. Range: 1..100", default=100, type=int)
        self.parser.add_argument("-m", "--led-gpio-mapping", help="Hardware Mapping: regular, adafruit-hat, adafruit-hat-pwm" , choices=['regular', 'adafruit-hat', 'adafruit-hat-pwm'], type=str)
        self.parser.add_argument("--led-scan-mode", action="store", help="Progressive or interlaced scan. 0 Progressive, 1 Interlaced (default)", default=1, choices=range(2), type=int)
        self.parser.add_argument("--led-pwm-lsb-nanoseconds", action="store", help="Base time-unit for the on-time in the lowest significant bit in nanoseconds. Default: 130", default=130, type=int)
        self.parser.add_argument("--led-show-refresh", action="store_true", help="Shows the current refresh rate of the LED panel")
        self.parser.add_argument("--led-slowdown-gpio", action="store", help="Slow down writing to GPIO. Range: 0..4. Default: 1", default=1, type=int)
        self.parser.add_argument("--led-no-hardware-pulse", action="store", help="Don't use hardware pin-pulse generation")
        self.parser.add_argument("--led-rgb-sequence", action="store", help="Switch if your matrix has led colors swapped. Default: RGB", default="RGB", type=str)
        self.parser.add_argument("--led-pixel-mapper", action="store", help="Apply pixel mappers. e.g \"Rotate:90\"", default="", type=str)
        self.parser.add_argument("--led-row-addr-type", action="store", help="0 = default; 1=AB-addressed panels;2=row direct", default=0, type=int, choices=[0,1,2])
        self.parser.add_argument("--led-multiplexing", action="store", help="Multiplexing type: 0=direct; 1=strip; 2=checker; 3=spiral; 4=ZStripe; 5=ZnMirrorZStripe; 6=coreman; 7=Kaler2Scan; 8=ZStripeUneven (Default: 0)", default=0, type=int)

    def usleep(self, value):
        time.sleep(value / 1000000.0)

    def initialize(self):
        # Format is:
        #           +-----Start------+  +-----End--------+  +--Start-----+ +----End-----+
        #   (class, (year, month, day), (year, month, day), (hour, minute),(hour, minute),  modPriority, time uninterrupted, initial value, Object)
        self.schedule = [
            [MatrixImagePlayground, (2023, 1, 1),   (2030, 12, 31),  (7, 0),  (7, 1),   1, 50, 15, None],       # Start the day with a 'Ready for the day?' sign for one minute!
            [MatrixImagePlayground, (2021, 1, 1),   (2030, 12, 31),  (7, 0),  (7, 2),   1, 20, 17, None],       # Show the school logo for 20 seconds 
            [MatrixSprite,          (2021, 1, 1),   (2030, 12, 31),  (7, 0),  (7, 30),  1, 10,  (0, "Good", "morning!"), None],       # Adabot in the morning
            [MatrixImagePlayground, (2023, 8, 2),   (2023,  8,  2),  (7, 0),  (8, 45),  1, 10, 11, None],       # Welcome back to school on the first day of school!
            [MatrixWeatherAndTime,  (2021, 1, 1),   (2030, 12, 31),  (7, 0),  (21, 58), 1, 60,  1, None],       # Standard time and weather all day, until 9:58, when we're ready to turn in for the night!
            [MatrixImagePlayground, (2023, 12, 14), (2023, 12, 26),  (7, 0),  (23, 59), 2, 15, 10, None],       # Christmas Tree at Christmas time
            [MatrixImagePlayground, (2024, 2, 14),  (2024, 2, 15),   (8, 15), (4, 49),  2, 20, 16, None],       # Valentine's Day
            [MatrixSprite,          (2021, 1, 1),   (2030, 12, 31),  (9, 45), (23, 59), 3, 15,  0, None],       # Adabot for the middle of the day
#            [MatrixScroller, (2021, 8, 1), (2030, 12, 31),  (6, 0), (23, 59), 3, 10, 1, None],
            [MatrixImagePlayground, (2021, 1, 1), (2030, 12, 31), (8, 15), (23, 59), 10, 10, 17, None],
            [MatrixImagePlayground, (2022, 8, 15),  (2030, 12, 31),  (11, 15), (13, 0), 1, 20, -2, None],         # Lunch Time - show what is being served for lunch
            [MatrixSprite,          (2021, 1, 1),   (2030, 12, 31),  (21, 59), (23, 59), 1, 60, 2, None],       # Goodnight monster!
            [MatrixImagePlayground, (2021, 1, 1), (2030, 12, 31), (7, 0), (8, 15), 1, 20, -3, None],
#            [MatrixScroller, (2021, 1, 1), (2030, 12, 31), (8, 15), (23, 59), 2, 60, 0, None],
            [MatrixSpriteViewer, (2021, 1, 1), (2030, 12, 31), (7, 0), (7, 45), 1, 20, -1, None],
            [MatrixSpriteViewer, (2021, 1, 1), (2030, 12, 31), (2, 0), (23, 59), 3, 20, -1, None],
           [MatrixGifPlayer, (2021, 1, 1), (2030, 12, 31), (9, 0), (23, 59), 10, 30, 19, None],
#            [MatrixGifPlayer, (2021, 1, 1), (2030, 12, 31), (6, 0), (23, 59), 1, 30, (-1, True), None],
        ]
        self.entryNumber = 0
        self.count = 0

    def scheduler(self, switchFlag):
        now = datetime.now()
        hour = now.timetuple()[3]
        # Turn off the screen between 10 PM and 7 AM
        if switchFlag == 2:
            print("Switchflag was 2!")
        if hour >= 22 or hour <= 6:
            self.matrixBase = MatrixBase()
            self.matrix.Clear()
            self.doubleBuffer = self.matrix.SwapOnVSync(self.doubleBuffer)
            self.matrix.Clear()
            self.matrixBase.initialize(64, 32, self.doubleBuffer)
            self.doubleBuffer = self.matrix.SwapOnVSync(self.doubleBuffer)
        elif now < self.changeTime and switchFlag < 2:
            # It's not time to change yet, so don't do anything.
            return
        else:
            startNumber = 0
            print("Switch time")
            bFound = False
            while startNumber < len(self.schedule) and not bFound:
                entry = self.schedule[self.entryNumber]
                startDate = date(entry[1][0], entry[1][1], entry[1][2])
                endDate = date(entry[2][0], entry[2][1], entry[2][2])
                startTime = time(entry[3][0], entry[3][1])
                endTime = time(entry[4][0], entry[4][1])
                if now.date() >= startDate and now.date() < endDate and now.time() >= startTime and now.time() < endTime and (self.count % entry[5] == 0):
                    print("Switching to", self.entryNumber, entry[0])
                    if entry[8] is None:
                        entry[8] = entry[0](entry[7])
                        self.matrixBase = entry[8]
                        self.doubleBuffer.Clear()
                        self.matrixBase.initialize(64, 32, self.doubleBuffer)
                    else:
                        self.matrixBase = entry[8]
                        self.doubleBuffer.Clear()
                        self.matrixBase.restart(self.doubleBuffer)
                    self.doubleBuffer = self.matrix.SwapOnVSync(self.doubleBuffer)
                    self.changeTime = now + timedelta(seconds=entry[6])
                    bFound = True
                self.entryNumber = (self.entryNumber + 1) % len(self.schedule)
                if self.entryNumber == 0:
                    self.count = (self.count + 1) % 20790
                    print("Count", self.count)
                startNumber = startNumber + 1
            if startNumber == len(self.schedule) and not bFound:
                print("Went through entire list and didn't find anything to show. Showing default.")
                self.matrixBase = MatrixDateTime(0)
                #self.matrixBase = MatrixAB(0)
                #self.matrixBase = MatrixWeather(0)
                self.matrixBase.initialize(64, 32, self.doubleBuffer)
                self.doubleBuffer = self.matrix.SwapOnVSync(self.doubleBuffer)
                self.changeTime = now + timedelta(minutes=2)
            # If we've gone through the entire list, now we can incremement count

    def run(self):
        print("Running")
        self.doubleBuffer = self.matrix.CreateFrameCanvas()
        #self.matrixBase = MatrixAB(0)
        self.matrixBase = MatrixBase()
        #self.matrixBase = MatrixSprite(3)
        #self.matrixBase = MatrixImagePlayground(8)
        #self.matrixBase = MatrixScroller(0)
        #self.matrixBase = MatrixSpriteViewer(random.randint(0,4))
        #self.matrixBase = MatrixGifPlayer(-1)
        #self.matrixBase = MatrixStayOnTarget(0)
        #self.matrixBase = MatrixWeather(0)
        #self.matrixPointer = self.matrixBase
        self.matrixBase.initialize(64, 32, self.doubleBuffer)
        self.matrix.Clear()
        self.doubleBuffer = self.matrix.SwapOnVSync(self.doubleBuffer)
        self.changeTime = datetime.now() + timedelta(seconds=20)
        font = graphics.Font()
        font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/5x8.bdf")
        self.matrix.Clear()

        hostname = socket.gethostname()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(("8.8.8.8",80))
            ip_address = s.getsockname()[0]
            ip = ip_address.split(".")
            offset = 8
            #ip_address = socket.gethostbyname(hostname)
            #ip_address = socket.getsockname()[0]
            for num in ip:
                graphics.DrawText(self.doubleBuffer, font, 10, offset, graphics.Color(244,244, 10), num)
                offset += 8
        except Exception as err:
            graphics.DrawText(self.doubleBuffer, font, 1, 18, graphics.Color(255, 0, 0), "No Network")
        
        #length = graphics.DrawText(self.doubleBuffer, font, 1,12, graphics.Color(225, 255, 0), ip_address)
        #length = graphics.DrawText(self.doubleBuffer, font, 1, 27, graphics.Color(0, 255, 0), hostname)
        self.doubleBuffer = self.matrix.SwapOnVSync(self.doubleBuffer)
        # Initialize other classes and then keep them around??
        bSwitched = 0
        while True:
            # Or just re-create them each time they are needed??
            self.scheduler(bSwitched)
            bSwitched = self.matrixBase.run(self.doubleBuffer)
            if bSwitched == 2:
                print('bSwitched == 2')
            if bSwitched > 0:
                self.doubleBuffer = self.matrix.SwapOnVSync(self.doubleBuffer)

    def process(self):
        self.args = self.parser.parse_args()

        options = RGBMatrixOptions()

        if self.args.led_gpio_mapping != None:
            options.hardware_mapping = self.args.led_gpio_mapping
        options.rows = self.args.led_rows
        options.cols = self.args.led_cols
        options.chain_length = self.args.led_chain
        options.parallel = self.args.led_parallel
        options.row_address_type = self.args.led_row_addr_type
        options.multiplexing = self.args.led_multiplexing
        options.pwm_bits = self.args.led_pwm_bits
        options.brightness = self.args.led_brightness
        options.pwm_lsb_nanoseconds = self.args.led_pwm_lsb_nanoseconds
        options.led_rgb_sequence = self.args.led_rgb_sequence
        options.pixel_mapper_config = self.args.led_pixel_mapper
        if self.args.led_show_refresh:
            options.show_refresh_rate = 1

        if self.args.led_slowdown_gpio != None:
            options.gpio_slowdown = self.args.led_slowdown_gpio
        if self.args.led_no_hardware_pulse:
            options.disable_hardware_pulsing = True

        self.matrix = RGBMatrix(options = options)

        self.initialize()
        try:
            # Start loop
            print("Press CTRL-C to stop sample")
            self.run()
        except KeyboardInterrupt:
            print("Exiting\n")
            sys.exit(0)

        return True

# Main function
# e.g. call with
#  sudo ./matrixDriver.py --led-rows 32 --led-cols 64 --led-slowdown-gpio 4
if __name__ == "__main__":
    matrixDriver = MatrixDriver()
    if (not matrixDriver.process()):
        matrixDriver.print_help()
