# coding=utf-8
import random
import gameEngine
import entity
import pyglet


class Level(object):
    def __init__(self):
        self.platforms = []
        self.platformSize = 100
        self.generate(0)
        self.player = entity.Player()

    def render(self):
        self.player.render()
        for i in self.platforms:
            i.render()

    def simulate(self, dt):
        self.player.move(dt)
        
        if self.player.dy <= 0:
            for platform in self.platforms:
                if platform.jump(self.player):
                    break

    def generate(self, y):

        # # - Type 1
        # for i in xrange(y, gameEngine.GameEngine.W_HEIGHT, 25):
        #     platformRand = random.randint(0, gameEngine.GameEngine.W_WIDTH)
        #     if platformRand >= gameEngine.GameEngine.W_WIDTH / 1.4:
        #         posRand = random.randint(0, gameEngine.GameEngine.W_WIDTH)
        #         self.platforms.append(entity.Platform(posRand, i, self.platformSize, 5))

        # - Type 2
        for i in xrange(y, gameEngine.GameEngine.W_HEIGHT, int(gameEngine.GameEngine.W_WIDTH / 20)):
            posRand = random.randint(0, gameEngine.GameEngine.W_WIDTH)
            self.platforms.append(entity.Platform(posRand, i, self.platformSize, 5))
