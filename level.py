# coding=utf-8
import random
import gameEngine
import entity
# import pyglet


class Level(object):
    def __init__(self):
        self.platforms = []
        self.ennemis = []
        self.platformSize = 64
        self.player = entity.Player()
        self.generate(0)
        self.generate(gameEngine.GameEngine.W_HEIGHT)
        self.lastGeneration = gameEngine.GameEngine.W_HEIGHT * 2
        self.score = 0
        self.bullets = []

    def render(self):
        if self.player.isDead:
            pass
        else:
            self.player.render()
            for i in self.platforms:
                i.render()
        for i in self.ennemis:
            i.render()

        for bullet in self.bullets:
            bullet.render()

    def simulate(self, dt):
        if self.player.isDead:
            pass
        else:

            for i in self.platforms:
                if i.isMoving:
                    i.simulate(dt)

            self.player.move(dt)
            self.player.shoot(self.bullets)

            if self.player.y > self.score:
                self.score = self.player.y

            if self.player.dy <= 0:
                for platform in self.platforms:
                    if platform.jump(self.player):
                        self.generate(self.lastGeneration)
                        break

            for bullet in self.bullets:
                bullet.simulate(dt)
                for i in self.ennemis:
                    if i.collide(bullet):
                        self.ennemis.remove(i)
                        self.bullets.remove(bullet)

            for i in self.ennemis:
                i.simulate(dt)
                if i.collide(self.player):
                    if self.player.dy < 0:
                        self.ennemis.remove(i)
                        self.player.startJumpY = i.y + i.height
                        self.player.timeJumping = 0
                        break
                    else:
                        self.player.isDead = True

    def generate(self, y):

        # # - Type 1
        # for i in xrange(y, gameEngine.GameEngine.W_HEIGHT, 25):
        #     platformRand = random.randint(0, gameEngine.GameEngine.W_WIDTH)
        #     if platformRand >= gameEngine.GameEngine.W_WIDTH / 1.4:
        #         posRand = random.randint(0, gameEngine.GameEngine.W_WIDTH)
        #         self.platforms.append(entity.Platform(posRand, i, self.platformSize, 5))

        # - Type 2
        for i in xrange(y, y + gameEngine.GameEngine.W_HEIGHT, int(gameEngine.GameEngine.W_WIDTH / 15)):
            if i < self.player.y + gameEngine.GameEngine.W_HEIGHT * 2:
                posRand = random.randint(0, gameEngine.GameEngine.W_WIDTH)
                randPlatform = random.randint(0, 5)
                if randPlatform == 0:
                    self.platforms.append(entity.FallingPlatform(posRand, i, self.platformSize, 10))
                elif randPlatform >= 4:
                    self.platforms.append(entity.Platform(posRand, i, self.platformSize, 10))
                else:
                    self.platforms.append(entity.MovingPlatform(posRand, i, self.platformSize, 10))
                self.lastGeneration = i + gameEngine.GameEngine.W_WIDTH / 15
                if not random.randint(0, 1) and i > gameEngine.GameEngine.W_WIDTH:
                    print i
                    posRand = random.randint(0, gameEngine.GameEngine.W_WIDTH)
                    self.ennemis.append(entity.Ennemy(posRand, i))

        for i in self.platforms:
            if i.y < self.player.y - gameEngine.GameEngine.W_HEIGHT:
                self.platforms.remove(i)
        print len(self.platforms)
