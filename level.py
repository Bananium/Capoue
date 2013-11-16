# coding=utf-8
import random
import gameEngine
import entity
# import pyglet
try:
    range = xrange
except NameError:
    pass


class Level(object):
    def __init__(self):
        self.platforms = []
        self.ennemis = []
        self.items = []
        self.bullets = []
        self.score = 0

        self.platformSize = 64

        self.player = entity.Player()
        self.generate(0)
        self.generate(gameEngine.GameEngine.W_HEIGHT)
        self.lastGeneration = gameEngine.GameEngine.W_HEIGHT * 2

    def render(self):
        if self.player.isDead:
            return
        else:
            for i in self.platforms:
                i._render()
            for i in self.ennemis:
                i.render()
            for bullet in self.bullets:
                bullet.render()
            for i in self.items:
                i.render()
            self.player.render()

    def simulate(self, dt):
        if self.player.isDead:
            return
        else:
            for i in self.platforms:
                i._simulate(dt)

        self.player.move(dt)
        if self.player.y > self.score:
            self.score = self.player.y
        for i in self.ennemis:
            if i.y < self.player.y - gameEngine.GameEngine.W_HEIGHT:
                self.ennemis.remove(i)
                continue
            i.simulate(dt)
            if i.collide(self.player):
                if self.player.dy < 0:
                    self.ennemis.remove(i)
                    self.player.startJumpY = i.y + i.height
                    self.player.timeJumping = 0
                    break
                else:
                    self.player.isDead = True
        if self.player.item is not None:
            self.generate(self.lastGeneration)
        else:
            self.player.shoot(self.bullets)

            if self.player.dy <= 0:
                for platform in self.platforms:
                    if platform.jump(self.player):
                        self.generate(self.lastGeneration)
                        break

            for bullet in self.bullets:
                bullet.simulate(dt)
                if bullet.y > self.player.y + gameEngine.GameEngine.W_HEIGHT:
                    self.bullets.remove(bullet)
                else:
                    for i in self.ennemis:
                        if i.collide(bullet):
                            self.ennemis.remove(i)
                            self.bullets.remove(bullet)

            for i in self.items:
                if i.y < self.player.y - gameEngine.GameEngine.W_HEIGHT * 2:
                    self.items.remove(i)
                    continue
                if i.collide(self.player):
                    self.items.remove(i)
                    self.player.item = i

    def generate(self, y):
        blinking = not random.randint(0, 15)
        for i in range(int(y), int(y + gameEngine.GameEngine.W_HEIGHT), int(gameEngine.GameEngine.W_HEIGHT / 8)):
            if i < self.player.y + gameEngine.GameEngine.W_HEIGHT * 2:
                self.lastGeneration = i + gameEngine.GameEngine.W_WIDTH / 15
                posRand = random.randint(0, gameEngine.GameEngine.W_WIDTH)
                randPlatform = random.randint(0, 10)
                if not randPlatform:
                    self.platforms.append(entity.BlinkingPlatform(posRand, i, self.platformSize, 10, 0, 1))  # Sadique: Elles clignotent tout le temps :D
                elif 1 < randPlatform < 3:
                    self.platforms.append(entity.FallingPlatform(posRand, i, self.platformSize, 10, blinking))
                elif randPlatform >= 6:
                    self.platforms.append(entity.Platform(posRand, i, self.platformSize, 10, blinking))
                    if not random.randint(0, 10) and i > gameEngine.GameEngine.W_WIDTH:
                        self.items.append(entity.JetPack(posRand + (self.platformSize - entity.JetPack.WIDTH) / 2, i + 10))
                        continue  # If jetpack, no ennemies
                else:
                    self.platforms.append(entity.MovingPlatform(posRand, i, self.platformSize, 10, random.randint(0, 1), blinking))
                if not random.randint(0, 1) and i > gameEngine.GameEngine.W_WIDTH:
                    posRand = random.randint(0, gameEngine.GameEngine.W_WIDTH)
                    self.ennemis.append(entity.Ennemy(posRand, i, random.randint(0, 1)))

        for i in self.platforms:
            if i.y < self.player.y - gameEngine.GameEngine.W_HEIGHT:
                self.platforms.remove(i)
