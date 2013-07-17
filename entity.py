# -*- encoding: UTF-8 -*-

import gameEngine
import math
import time
from pyglet.gl import *  # parce les pyglet.gl.GLMACHIN non merci


class Platform(object):
    def __init__(self, x, y, width=20, height=100):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.isMoving = False

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
        pass


class MovingPlatform(Platform):
    def __init__(self, x, y, width=20, height=100):
        super(MovingPlatform, self).__init__(x, y, width, height)
        self.isMoving = True
        self.movementDirection = "Right"
        self.speed = 100

    def simulate(self, dt):
        if self.x < gameEngine.GameEngine.W_WIDTH - self.width and self.movementDirection == "Right":
            self.x += self.speed * dt
        elif self.x > gameEngine.GameEngine.W_WIDTH - self.width and self.movementDirection == "Right":
            self.movementDirection = "Left"
        elif 0 < self.x and self.movementDirection == "Left":
            self.x -= self.speed * dt
        else:
            self.movementDirection = "Right"


class FallingPlatform(Platform):
        def __init__(self, x, y, width=20, height=100):
            super(FallingPlatform, self).__init__(x, y, width, height)
            self.isMoving = True
            self.isFalling = False
            self.speed = 250

        def jump(self, player):
            y = player.y - player.dy
            while y > player.y + player.dy:

                if self.x < player.getX() < self.x + self.width and self.y < y < self.y + self.height:
                    player.startJumpY = self.y + self.height
                    player.timeJumping = 0
                    self.isFalling = True
                    return True

                elif self.x < player.getX() + player.WIDTH < self.x + self.width and self.y < y < self.y + self.height:
                    player.startJumpY = self.y + self.height
                    player.timeJumping = 0
                    self.isFalling = True
                    return True

                y += player.dy / 10.0
            return False

        def simulate(self, dt):
            if self.isFalling:
                self.y -= self.speed * dt


class Ennemy(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.movementDirection = "Right"
        self.speed = 100
        self.health = 1

    def collide(self, ent):
        if self.x <= ent.getX() <= self.x + self.width or self.x <= ent.getX()+Player.WIDTH <= self.x + self.width:
            if self.y <= ent.y <= self.y + self.height or self.y <= ent.y+Player.HEIGHT <= self.y + self.height:
                return True
            elif ent.y <= self.y <= ent.y+Player.HEIGHT or ent.y <= self.y + self.height <= ent.y+Player.HEIGHT:
                return True

        elif ent.getX() <= self.x <= ent.getX()+Player.WIDTH or ent.getX() <= self.x + self.width <= ent.getX()+Player.WIDTH:
            if (self.y <= ent.y <= self.y + self.height) or (self.y <= ent.y+Player.HEIGHT <= self.y + self.height):
                return True
            elif ent.y <= self.y <= ent.y+Player.HEIGHT or ent.y <= self.y + self.height <= ent.y+Player.HEIGHT:
                return True
        return False

    def simulate(self, dt):
        if self.x < gameEngine.GameEngine.W_WIDTH - self.width and self.movementDirection == "Right":
            self.x += self.speed * dt
        elif self.x > gameEngine.GameEngine.W_WIDTH - self.width and self.movementDirection == "Right":
            self.movementDirection = "Left"
        elif 0 < self.x and self.movementDirection == "Left":
            self.x -= self.speed * dt
        else:
            self.movementDirection = "Right"

    def render(self):
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.width, self.y)
        glVertex2f(self.x + self.width, self.y + self.height)
        glVertex2f(self.x, self.y + self.height)
        glEnd()


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

        self.isDead = False

        self.fireRate = 10.0
        self.lastShoot = time.time()

        self.isShooting = False

    def move(self, dt):
        xBefore, yBefore = self.x, self.y

        # Deplacement en x
        dx = self.cursorPosX - self.x

        if dx > 400:
            dx = 400

        self.x = (self.x + dx * dt * math.log(math.sqrt(dx**2)/50 + 2))

        # deplacement en y
        self.timeJumping += dt * 7
        self.y = (- 9.81 * self.timeJumping**2 + self.velY * self.timeJumping + self.startJumpY)

        self.dy = self.y - yBefore

    def shoot(self, bullets):
        if time.time() - self.lastShoot > 1/self.fireRate and self.isShooting:
            bullets.append(Bullet(self.getX() + self.WIDTH/2, self.y, 0, 1000))
            self.lastShoot = time.time()

    def getX(self):
        return self.x % gameEngine.GameEngine.W_WIDTH

    def render(self):
        glBegin(GL_QUADS)
        glVertex2f(self.getX(), self.y)
        glVertex2f(self.getX() + self.WIDTH, self.y)
        glVertex2f(self.getX() + self.WIDTH, self.y + self.HEIGHT)
        glVertex2f(self.getX(), self.y + self.HEIGHT)
        glEnd()


class Bullet(object):
    WIDTH = 10
    HEIGHT = 10

    def __init__(self, x, y, xVel, yVel):
        self.x = x
        self.y = y 
        self.xVel = xVel
        self.yVel = yVel

    def simulate(self, dt):
        self.x += self.xVel * dt
        self.y += self.yVel * dt

    def render(self):
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.WIDTH, self.y)
        glVertex2f(self.x + self.WIDTH, self.y + self.HEIGHT)
        glVertex2f(self.x, self.y + self.HEIGHT)
        glEnd()
