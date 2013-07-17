# coding=utf-8
import random
import gameEngine


class Level(object):
    def __init__(self):
        self.platforms = []
        self.platformSize = 100
        self.generate(0)

    def render(self):
        for i in self.platforms:
            i.render()

    def simulate(self, dt):
        pass

    def generate(self, y):
        for i in xrange(y, gameEngine.GameEngine.W_HEIGHT, 10):
            platformRand = random.randint(0, 100)
            print platformRand
