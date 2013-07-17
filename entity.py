# -*- encoding: UTF-8 -*-

import time
import gameEngine
import math
from pyglet.gl import *  # parce les pyglet.gl.GLMACHIN non merci


class Platform(object):
    def __init__(self, x, y, width=20, height=100):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def render(self):
        glBegin(GL_QUADS)
        glVertex2i(self.x, self.y)
        glVertex2i(self.x + self.width, self.y)
        glVertex2i(self.x + self.width, self.y + self.height)
        glVertex2i(self.x, self.y + self.height)
        glEnd()


class Player(object):

    WIDTH = 48
    HEIGHT = 48

    def __init__(self):
        self.x = 0
        self.y = 0

        self.dy = 0

        self.startJumpY = 0
        self.cursorPosX = 0

    def move(self, dt):
        xBefore, yBefore = self.x, self.y

        # Deplacement en x
        dx = self.cursorPosX - self.x
        self.x = (self.x + dx / math.log(math.sqrt(dx**2) * 1000 + 100000)) % gameEngine.GameEngine.W_WIDTH

    def render(self):
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.WIDTH, self.y)
        glVertex2f(self.x + self.WIDTH, self.y + self.HEIGHT)
        glVertex2f(self.x, self.y + self.HEIGHT)
        glEnd()


# 1/2 * g * t^2 + v0 * t + pos0
