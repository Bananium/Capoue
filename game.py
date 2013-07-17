# coding=utf-8
import level

class Game(object):
    def __init__(self):
        self.level = level.Level()

    def render(self):
        self.level.render()

    def simulate(self, dt):
        self.level.simulate(dt)
