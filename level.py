# coding=utf-8
import entity

class Level(object):
    def __init__(self):
        self.player = entity.Player()

    def render(self):
        self.player.render()

    def simulate(self, dt):
        self.player.move(dt)
