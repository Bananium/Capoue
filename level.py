# coding=utf-8
import random
import gameEngine
import entity
# import pyglet


class Level(object):
    def __init__(self):
        self.platforms = []
        self.platformSize = 100
        self.player = entity.Player()
        self.generate(0)
        self.lastGeneration = gameEngine.GameEngine.W_HEIGHT

    def render(self):
        self.player.render()
        for i in self.platforms:
            i.render()

    def simulate(self, dt):
        for i in self.platforms:
            if i.isMoving:
                i.simulate(dt)

        self.player.move(dt)

        if self.player.dy <= 0:
            for platform in self.platforms:
                if platform.jump(self.player):
                    self.generate(self.lastGeneration)
                    break

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
                    self.platforms.append(entity.FallingPlatform(posRand, i, self.platformSize, 5))
                elif randPlatform >= 4:
                    self.platforms.append(entity.Platform(posRand, i, self.platformSize, 5))
                else:
                    self.platforms.append(entity.MovingPlatform(posRand, i, self.platformSize, 5))
                self.lastGeneration = i + gameEngine.GameEngine.W_WIDTH / 15
        for i in self.platforms:
            if i.y < self.player.y - gameEngine.GameEngine.W_HEIGHT:
                self.platforms.remove(i)
        print len(self.platforms)
