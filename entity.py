# -*- encoding: UTF-8 -*-

import gameEngine
import math
import time
import random
from pyglet.gl import *  # parce les pyglet.gl.GLMACHIN non merci
import types

try:
    range = xrange
except NameError:
    pass


class Platform(object):
    def __init__(self, x, y, width=20, height=100, blinking=False):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.blinking = blinking
        self.isMoving = False
        self.isFalling = False
        self.shown = True
        self.type = "Normal"
        self.tick = 0
        self.blinkTick = 0

    def jump(self, player):
        y = player.y - player.dy
        while y > player.y + player.dy:
            if self.x < player.getX() < self.x + self.width and self.y < y < self.y + self.height or \
               self.x < player.getX() + player.WIDTH < self.x + self.width and self.y < y < self.y + self.height:
                player.startJumpY = self.y + self.height
                player.timeJumping = 0
                return True

            y += player.dy / 10.0

        return False

    def _render(self):
        if self.blinkTick < 50 and self.blinking:
            self.shown = True
        elif 50 <= self.blinkTick < 100 and self.blinking:
            self.shown = False
        else:
            self.blinkTick = 0

        if self.shown:
            if self.type == "Normal":
                glColor4f(0.3, 0.8, 0.3, 1)
            elif self.type == "Moving":
                glColor4f(0.2, 0.5, 1, 1)
            elif self.type == "Booming":
                glColor4f(0.5, 0.7, 0.5, 1)
            else:
                glColor4f(1, 0.6, 0.3, 1)

            glBegin(GL_QUADS)
            glVertex2f(self.x, self.y)
            glVertex2f(self.x + self.width, self.y)
            glVertex2f(self.x + self.width, self.y + self.height)
            glVertex2f(self.x, self.y + self.height)
            glEnd()

        self.render()

    def _simulate(self, dt):
        self.blinkTick += 1
        self.tick += 1
        self.simulate(dt)

    def simulate(self, dt):
        pass

    def render(self):
        pass


class EnlargingPlatform(Platform):
    def __init__(self, x, y, width=20, height=100, dir=0, blinking=False):
        super(EnlargingPlatform, self).__init__(x, y, width, height, blinking)
        self.enlargissement = "+"

    def simulate(self, dt):
        if self.enlargissement == "+":
            self.width += 1
            self.x -= 0.5
            if self.width > 125:
                self.enlargissement = "-"
        else:
            self.width -= 1
            self.x += 0.5
            if self.width < 25:
                self.enlargissement = "+"


class BoomingPlatform(Platform):
    def __init__(self, x, y, width=20, height=100, dir=0, blinking=False):
        super(BoomingPlatform, self).__init__(x, y, width, height, blinking)
        self.type = "Booming"
        self.particles = []
        self.exploded = False

    def jump(self, player):
        if super(BoomingPlatform, self).jump(player) and not player.isDead:
            player.isDead = True
            self.exploded = True
            self.shown = False
            self.blinking = False
            for j in range(1, 4):
                for i in range(25):
                    angle = 6.28 * random.random()
                    self.particles.append(Particle(self.x + self.width / 2, self.y + self.height / 2, 10, 10, (math.cos(angle), math.sin(angle)), j))

    def render(self):
        if self.exploded:
            for i in self.particles:
                i.render()

    def simulate(self, dt):
        for i in self.particles:
            i.simulate(dt)


class Particle:
    def __init__(self, x, y, width, height, vec, speed):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vec = vec
        self.speed = speed * 100
        if not random.randint(0, 1):
            self.color = (0.5, 0.7, 0.5, 1)
        else:
            self.color = (1, 1, 1, 1)

    def render(self):
        glColor4f(self.color[0], self.color[1], self.color[2], self.color[3])

        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.width, self.y)
        glVertex2f(self.x + self.width, self.y + self.height)
        glVertex2f(self.x, self.y + self.height)
        glEnd()

    def simulate(self, dt):
        self.x += self.vec[0] * dt * self.speed
        self.y += self.vec[1] * dt * self.speed


class MovingPlatform(Platform):
    # Dir: 0 => Left
    #    : 1 => Right
    def __init__(self, x, y, width=20, height=100, dir=0, blinking=False):
        super(MovingPlatform, self).__init__(x, y, width, height, blinking)
        self.movementDirection = "Right" if dir else "Left"
        self.speed = max(100, min(self.y * 0.01, 500))
        self.type = "Moving"

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
        def __init__(self, x, y, width=20, height=100, blinking=False):
            super(FallingPlatform, self).__init__(x, y, width, height, blinking)
            self.speed = 250
            self.type = "Falling"

        def jump(self, player):
            if super(FallingPlatform, self).jump(player):
                player.velY = 100
                self.isFalling = True
                return True
            return False

        def simulate(self, dt):
            if self.isFalling:
                self.y -= self.speed * dt


class BlinkingPlatform(BoomingPlatform, FallingPlatform, MovingPlatform, Platform):
    def __init__(self, x, y, width=20, height=100, dir=0, blinking=False):
        super(BlinkingPlatform, self).__init__(x, y, width, height, blinking)
        self.movementDirection = "Right" if dir else "Left"
        self.speed = max(100, min(self.y * 0.01, 500))

        self.blinking = blinking
        self.type = "Moving"

    def _simulate(self, dt):
        if not self.isFalling:
            if self.tick < 100:
                self.simulate = types.MethodType(MovingPlatform.simulate, self)
                self.jump = types.MethodType(MovingPlatform.jump, self)
                self.speed = max(100, min(self.y * 0.01, 500))
                self.type = "Moving"
            elif 100 <= self.tick < 200:
                self.simulate = types.MethodType(FallingPlatform.simulate, self)
                self.jump = types.MethodType(FallingPlatform.jump, self)
                self.speed = 250
                self.type = "Falling"
            elif 200 <= self.tick < 300:
                self.simulate = types.MethodType(BoomingPlatform.simulate, self)
                self.jump = types.MethodType(BoomingPlatform.jump, self)
                self.type = "Booming"
            else:
                self.tick = 0

        super(BlinkingPlatform, self)._simulate(dt)


class Ennemy(object):
    def __init__(self, x, y, dir=0):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.movementDirection = "Right" if dir else "Left"
        self.speed = max(25, min(self.x * 0.005, 100))
        self.health = 1

    def collide(self, ent):
        if self.x <= ent.getX() <= self.x + self.width or self.x <= ent.getX() + ent.WIDTH <= self.x + self.width:
            if self.y <= ent.y <= self.y + self.height or self.y <= ent.y + ent.HEIGHT <= self.y + self.height \
               or ent.y <= self.y <= ent.y + ent.HEIGHT or ent.y <= self.y + self.height <= ent.y + ent.HEIGHT:
                return True

        elif ent.getX() <= self.x <= ent.getX() + ent.WIDTH or ent.getX() <= self.x + self.width <= ent.getX() + ent.WIDTH:
            if self.y <= ent.y <= self.y + self.height or self.y <= ent.y + ent.HEIGHT <= self.y + self.height or \
               ent.y <= self.y <= ent.y + ent.HEIGHT or ent.y <= self.y + self.height <= ent.y + ent.HEIGHT:
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
        glColor4f(1, 0.3, 0.3, 1)
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
        self.x = gameEngine.GameEngine.W_WIDTH / 2
        self.y = 0

        self.dy = 0

        self.velY = 100

        self.timeJumping = 0
        self.startJumpY = 150
        self.cursorPosX = self.x

        self.isDead = False

        self.fireRate = 2.0
        self.lastShoot = time.time()

        self.isShooting = False

        self.item = None

    def move(self, dt):
        xBefore, yBefore = self.x, self.y

        # Deplacement en x
        dx = self.cursorPosX - self.x

        if dx > 400:
            dx = 400

        self.x = (self.x + dx * dt * math.log(math.sqrt(dx ** 2) / 50 + 2))

        if self.item is None:
            # deplacement en y
            self.timeJumping += dt * 7
            self.y = (- 9.81 * self.timeJumping ** 2 + self.velY * self.timeJumping + self.startJumpY)
        else:
            self.y += self.item.effectYVel * dt
            self.item.effectTime -= dt
            if self.item.effectTime <= 0:
                self.item = None
                self.timeJumping = 0
                self.startJumpY = self.y

        self.dy = self.y - yBefore

    def shoot(self, bullets):
        if time.time() - self.lastShoot > 1 / self.fireRate and self.isShooting:
            bullets.append(Bullet(self.getX() + self.WIDTH / 2, self.y + self.HEIGHT / 2, 0, 1000))
            self.lastShoot = time.time()

    def getX(self):
        return self.x % gameEngine.GameEngine.W_WIDTH

    def render(self):
        glColor4f(1, 1, 1, 1)
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

    def getX(self):
        return self.x

    def render(self):
        glBegin(GL_QUADS)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.WIDTH, self.y)
        glVertex2f(self.x + self.WIDTH, self.y + self.HEIGHT)
        glVertex2f(self.x, self.y + self.HEIGHT)
        glEnd()


class JetPack(object):
    WIDTH = 20
    HEIGHT = 20

    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.effectYVel = 725
        self.effectTime = 5

    def render(self):
        glBegin(GL_QUADS)
        glColor4f(1, 0.6, 1, 1)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x + self.WIDTH, self.y)
        glVertex2f(self.x + self.WIDTH, self.y + self.HEIGHT)
        glVertex2f(self.x, self.y + self.HEIGHT)
        glEnd()

    def collide(self, ent):
        if self.x <= ent.getX() <= self.x + self.WIDTH or self.x <= ent.getX() + ent.WIDTH <= self.x + self.WIDTH:
            if self.y <= ent.y <= self.y + self.HEIGHT or self.y <= ent.y + ent.HEIGHT <= self.y + self.HEIGHT \
               or ent.y <= self.y <= ent.y + ent.HEIGHT or ent.y <= self.y + self.HEIGHT <= ent.y + ent.HEIGHT:
                return True

        elif ent.getX() <= self.x <= ent.getX() + ent.WIDTH or ent.getX() <= self.x + self.WIDTH <= ent.getX() + ent.WIDTH:
            if self.y <= ent.y <= self.y + self.HEIGHT or self.y <= ent.y + ent.HEIGHT <= self.y + self.HEIGHT or \
               ent.y <= self.y <= ent.y + ent.HEIGHT or ent.y <= self.y + self.HEIGHT <= ent.y + ent.HEIGHT:
                return True
        return False
