#!/usr/bin/env python3
import time
import random
import struct
import sys
import os
import subprocess
from datetime import datetime, timedelta
from bluepy.btle import Scanner, DefaultDelegate, Peripheral, BTLEDisconnectError
import time
from samplebase import SampleBase
from PIL import Image
from rgbmatrix import graphics
from sprite import Sprite
from matrixImageShow import ImageShow
from matrixImageSequence import ImageSequence
from matrixSprite import MatrixSprite
from matrixDateTime import MatrixDateTime
from matrixOnAir import MatrixOnAir
from matrixBubbles import MatrixBubbles
from matrixMemorialOffice import MatrixMemorialOffice
from matrixScroller import MatrixScroller
from matrixBaseClass import MatrixBaseClass
from matrixWeather import MatrixWeather
from matrixImagePlayground import MatrixImagePlayground
from matrixSpriteViewer import MatrixSpriteViewer

def dump_services(dev):
    services = sorted(dev.services, key=lambda s: s.hndStart)
    for s in services:
        print ("\t%04x: %s" % (s.hndStart, s))
        if s.hndStart == s.hndEnd:
            continue
        chars = s.getCharacteristics()
        for i, c in enumerate(chars):
            props = c.propertiesToString()
            h = c.getHandle()
            if 'READ' in props:
                val = c.read()
                if c.uuid == btle.AssignedNumbers.device_name:
                    string = ANSI_CYAN + '\'' + \
                        val.decode('utf-8') + '\'' + ANSI_OFF
                elif c.uuid == btle.AssignedNumbers.device_information:
                    string = repr(val)
                else:
                    string = '<s' + binascii.b2a_hex(val).decode('utf-8') + '>'
            else:
                string = ''
            print ("\t%04x:    %-59s %-12s %s" % (h, c, props, string))

            while True:
                h += 1
                if h > s.hndEnd or (i < len(chars) - 1 and h >= chars[i + 1].getHandle() - 1):
                    break
                try:
                    val = dev.readCharacteristic(h)
                    print ("\t%04x:     <%s>" %
                           (h, binascii.b2a_hex(val).decode('utf-8')))
                except btle.BTLEException:
                    break

class MatrixDriver(SampleBase, DefaultDelegate):
    peripheral = None
    def __init__(self, *args, **kwargs):
        super(MatrixDriver, self).__init__(*args, **kwargs)
        self.TIME_TO_NEXT_SWITCH = time.monotonic()
        self.matrixBase = None
        self.screensaverTime = datetime.now() + timedelta(minutes=15)
        self.number = 0
        
    def shouldSwitch(self):
        self.NOW = time.monotonic()
        if (self.TIME_TO_NEXT_SWITCH - self.NOW) < 0:
            self.TIME_TO_NEXT_SWITCH = random.randint(5,10) + self.NOW
            r = random.randint(0,5)
            print(r)

            t = random.randint(0,3)
            if t == 0:
                self.matrixBase = ImageShow(r)
            elif t == 1:
                self.matrixBase = MatrixSprite(r)
            elif t == 2:
                self.matrixBase = MatrixDateTime(r)
            elif t == 3:
                self.matrixBase = MatrixOnAir(r)

            return True
        # Could look for messages here ...
        return False

    def run(self):
        self.double_buffer = self.matrix.CreateFrameCanvas()
        while True:
            if self.peripheral.waitForNotifications(0.001):
                # handleNotification() was called
                print("Inside waitForNotification")
            now = datetime.now()
            hour = now.timetuple()[3]
            if (hour >= 23 or hour <= 7) and (now > self.screensaverTime):
                self.matrixBase = MatrixBaseClass("0")
                self.matrix.Clear()
                self.double_buffer = self.matrix.SwapOnVSync(self.double_buffer)
                self.matrix.Clear()
                self.matrixBase.initialize(32, 64, self.double_buffer)
                self.double_buffer = self.matrix.SwapOnVSync(self.double_buffer)
            if self.matrixBase is None:
                self.matrixBase = MatrixDateTime(0)
                self.matrix.Clear()
                self.double_buffer = self.matrix.SwapOnVSync(self.double_buffer)
                self.matrix.Clear()
                self.matrixBase.initialize(32, 64, self.double_buffer)
                self.double_buffer = self.matrix.SwapOnVSync(self.double_buffer)
            bSwitched = self.matrixBase.run(self.double_buffer)
            if bSwitched:
                self.double_buffer = self.matrix.SwapOnVSync(self.double_buffer)
            '''
            if self.shouldSwitch():
                print("Switching")
                print("Call the init routine of class")
                self.matrix.Clear()
                double_buffer = self.matrix.SwapOnVSync(double_buffer)
                self.matrix.Clear()
                self.matrixBase.initialize(32, 64, double_buffer)
                double_buffer = self.matrix.SwapOnVSync(double_buffer)
            #print("Call the run routine of class")
            bSwitched = self.matrixBase.run(double_buffer)
            if bSwitched:
                double_buffer = self.matrix.SwapOnVSync(double_buffer)
            '''
    def checkForValidData(self, dev):
        for (adtype, desc, value) in dev.getScanData():
            if adtype == 255:
                # This is a manufacturer type
                if value[:4] == '2208':
                    print ("  %s = %s" % (desc, value))
                    print(" adtype: " , adtype)
                    print("Adafruit!")
                    if value[4:10] == '060000':
                        # Must be Adafruit Color, which we've commandeered
                        color = (int(value[14:16], 16), int(value[12:14], 16), int(value[10:12], 16))
                        print("Color", color)
                    return True
        return False

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
            self.checkForValidData(dev)
                
        elif isNewData:
            print ("Received new data from", dev.addr)
            self.checkForValidData(dev)
            
    def handleNotification(self, cHandle, data):
        # ... perhaps check cHandle
        # ... process 'data'
        val = struct.unpack('i', data)[0]
        if val == 0:
            # This is just the release of a button
            return
        print("val:", val)
        self.screensaverTime = datetime.now() + timedelta(minutes=15)
        if val & 0x1 == 0x1:
            self.matrixBase = ImageShow(0)
        elif val & 0x2 == 0x2:
            self.matrixBase = ImageShow(1)
        elif val & 0x4 == 0x4:
            self.matrixBase = ImageShow(2)
        elif val & 0x8 == 0x8:
            self.matrixBase = ImageShow(3)
        elif val & 0x10 == 0x10:
            self.matrixBase = ImageShow(4)
        elif val & 0x20 == 0x20:
            self.matrixBase = ImageShow(5)
        elif val & 0x40 == 0x40:
            self.matrixBase = MatrixImagePlayground(self.number)
        elif val & 0x80 == 0x80:
            self.matrixBase = MatrixSpriteViewer(self.number)
        elif val & 0x100 == 0x100:
            self.matrixBase = ImageSequence(self.number)
        elif val & 0x200 == 0x200:
            self.matrixBase = MatrixMemorialOffice(0)
        elif val & 0x400 == 0x400:
            self.matrixBase = MatrixScroller(self.number)
        elif val & 0x800 == 0x800:
            self.matrixBase = MatrixWeather(self.number)
        elif val & 0x2000 == 0x2000:
            self.matrixBase = MatrixDateTime(0)
        elif val & 0x1000 == 0x1000:
            self.matrixBase = MatrixSprite(self.number)
        elif val & 0x4000 == 0x4000:
            self.matrixBase = MatrixBubbles(0)
        elif val & 0x8000 == 0x8000:
            self.matrixBase = MatrixOnAir(self.number)
        print("Switching")
        print("Call the init routine of class")
        self.number = (self.number + 1) % 30
        self.matrix.Clear()
        self.double_buffer = self.matrix.SwapOnVSync(self.double_buffer)
        self.matrix.Clear()
        self.matrixBase.initialize(64, 32, self.double_buffer)
        self.double_buffer = self.matrix.SwapOnVSync(self.double_buffer)
        #print("Call the run routine of class")
        bSwitched = self.matrixBase.run(self.double_buffer)
        if bSwitched:
            self.double_buffer = self.matrix.SwapOnVSync(self.double_buffer)
        print(val)
        
    def bluetoothConnect(self):
        found = False
        scanner = Scanner().withDelegate(self)

        try:
            devices = scanner.scan(10.0)
            for dev in devices:
                for (adtype, desc, value) in dev.getScanData():
                    if adtype == 9 and value=='CPlay':
                        self.peripheral = Peripheral(dev)
                        self.peripheral.withDelegate(self)
                        serviceList = self.peripheral.getServices()
                        for service in serviceList:
                            characteristic = service.getCharacteristics()
                            for c in characteristic:
                                print(c.uuid, c.propertiesToString())
                                if c.uuid == "adaf0601-c332-42a8-93bd-25e905756cb8":
                                    print("This is the button Press service")
                                    # This line is what causes a notification to go out
                                    self.peripheral.writeCharacteristic(c.valHandle + 1, b"\x01\x00")
                                    
                                    #val = binascii.b2a_hex(c.read())
                                    #val = binascii.unhexlify(val)
                                    val = struct.unpack('i', c.read())[0]
                                    print(str(val) + " deg C")
                                if c.uuid == "adaf1101-c332-42a8-93bd-25e905756cb8":
                                    found = True
                                    print("This is the NeoTrellis service")
                                    # This line is what causes a notification to go out
                                    self.peripheral.writeCharacteristic(c.valHandle + 1, b"\x01\x00")
                                    
                                    #val = binascii.b2a_hex(c.read())
                                    #val = binascii.unhexlify(val)
                                    val = struct.unpack('i', c.read())[0]
                                    print(str(val) + " button values")
            return found
        except BTLEDisconnectError:
            print("Bluetooth disconnect error")
            return False
        except BrokenPipeError:
            print("Broken pipe error. I need a new pipe!")
            return False
        except KeyboardInterrupt:
            print("\nExiting\n")
            peripheral.disconnect()
            sys.exit(0)

if __name__ == "__main__":
    matrixDriver = MatrixDriver()
    while True:
        
        while not matrixDriver.bluetoothConnect():
            print("searching...")
            pass

        try:
            if not matrixDriver.process():
                matrixDriver.print_help()
        except BTLEDisconnectError:
            print("Bluetooth connection lost")
            matrixDriver.peripheral.disconnect()
            matrixDriver.matrix.Clear()
            

