# -*- encoding: UTF-8 -*-

# import time
import gameEngine
import math
from pyglet.gl import *  # parce les pyglet.gl.GLMACHIN non merci


class Platform(object):
    def __init__(self, x, y, width=20, height=100, isMoving=False):
        self.initX = x
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.isMoving = isMoving
        if isMoving:
            self.movementDirection = "Right"
            self.speed = 100

    def jump(self, player):
        y = player.y - player.dy
        while y > player.y + player.dy:

            if self.x < player.getX() < self.x + self.width and self.y < y < self.y + self.height:
                player.startJumpY = self.y + self.height
                player.timeJumping = 0
                return True

            elif self.x < player.getX() + player.WIDTH < self.x + self.width and self.y < y < self.y + self.height:
                player.startJumpY = self.y + self.height
                player.timeJumping = 0
                return True

            y += player.dy / 10.0

        return False

    def render(self):
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.width, self.y)
        glVertex2f(self.x + self.width, self.y + self.height)
        glVertex2f(self.x, self.y + self.height)
        glEnd()

    def simulate(self, dt):
        if self.x < self.initX + self.width and self.movementDirection == "Right":
            self.x += self.speed * dt
        elif self.x > self.initX + self.width and self.movementDirection == "Right":
            self.movementDirection = "Left"
        elif self.initX < self.x and self.movementDirection == "Left":
            self.x -= self.speed * dt
        else:
            self.movementDirection = "Right"


class Player(object):

    WIDTH = 32
    HEIGHT = 32

    def __init__(self):
        self.x = gameEngine.GameEngine.W_WIDTH/2
        self.y = 0

        self.dy = 0

        self.velY = 100

        self.timeJumping = 0
        self.startJumpY = 150
        self.cursorPosX = self.x

    def move(self, dt):
        xBefore, yBefore = self.x, self.y

        # Deplacement en x
        dx = self.cursorPosX - self.x
        self.x = (self.x + dx * dt * math.log(math.sqrt(dx**2)/10 + 2))

        # deplacement en y
        self.timeJumping += dt * 7
        self.y = (- 9.81 * self.timeJumping**2 + self.velY * self.timeJumping + self.startJumpY)

        self.dy = self.y - yBefore

    def getX(self):
        return self.x % gameEngine.GameEngine.W_WIDTH

    def render(self):
        glBegin(GL_QUADS)
        glVertex2f(self.getX(), self.y)
        glVertex2f(self.getX() + self.WIDTH, self.y)
        glVertex2f(self.getX() + self.WIDTH, self.y + self.HEIGHT)
        glVertex2f(self.getX(), self.y + self.HEIGHT)
        glEnd()
