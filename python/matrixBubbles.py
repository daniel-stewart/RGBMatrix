from datetime import datetime
import random
from PIL import Image
from rgbmatrix import graphics
from matrixBaseClass import MatrixBaseClass

blue = graphics.Color(0, 0, 255)
cyan = graphics.Color(0, 255, 255)
blueWhite = graphics.Color(128, 128, 255)
darkBlue = graphics.Color(0, 0, 128)

class CircleState:
    radius = 0
    x = 0
    y = 0
    dy = 0

class MatrixBubbles(MatrixBaseClass):
    def __init__(self, level):
        pass
    
    def randCircle(self, c, w, h):
        c.radius = random.randint(1, 12)
        c.x = random.randint(-c.radius, w + c.radius - 1)
        c.yint = c.y = h + c.radius
        c.dy = c.radius / -40.0   

    def newRandCircle (self, w, h):
        c = CircleState ()
        self.randCircle(c, w, h)
        return c

    # move a circle by it's given dy
    # when off screen, make a new circle
    def moveCircle (self, c, d, w, h):
        d.radius = c.radius
        d.x = c.x
        d.y = c.y + c.dy
        d.yint = int(d.y)
        if d.yint < -d.radius:
            self.randCircle(d, w, h)
       
    numCircles = 8
    oldCircles = []
    newCircles = []

    def initialize(self, width, height, double_buffer):
        # make arrays of circles, both initially identical
        self.width = width
        self.height = height
        for i in range(1, self.numCircles):
            c = self.newRandCircle (width, height)
            self.newCircles.append(c)
            d = CircleState ()
            d.x = c.x
            d.y = c.y
            d.radius = c.radius
            d.yint = c.yint
            d.dy = c.dy
            print(d.x, d.y, d.radius)
            self.oldCircles.append(d)
        for c in self.newCircles:
            print(c.x, c.y, c.radius)
            graphics.DrawCircle(double_buffer, c.x, c.y, c.radius, blue)
            graphics.DrawCircle(double_buffer, c.x, c.y, c.radius+1, blueWhite)
            

        
                
    def run(self, double_buffer):
        double_buffer.Clear()
        # move the circles
        for i in range(0, self.numCircles-1):
            self.moveCircle(self.oldCircles[i], self.newCircles[i], self.width, self.height)
        # erase only when moved
        for i in range(0, self.numCircles-1):
            if self.oldCircles[i].yint != self.newCircles[i].yint:
                graphics.DrawCircle(double_buffer, self.oldCircles[i].x, self.oldCircles[i].yint, self.oldCircles[i].radius, blue)
                graphics.DrawCircle(double_buffer, self.oldCircles[i].x, self.oldCircles[i].yint, self.oldCircles[i].radius+1, blueWhite)
        # draw
        for i in range(0, self.numCircles-1):
            graphics.DrawCircle(double_buffer, self.newCircles[i].x, self.newCircles[i].yint, self.newCircles[i].radius, blue)
            graphics.DrawCircle(double_buffer, self.newCircles[i].x, self.newCircles[i].yint, self.newCircles[i].radius+1, blueWhite)
        # swap old and new
        t = self.oldCircles
        self.oldCircles = self.newCircles
        self.newCircles = t
        return True
