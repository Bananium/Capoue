# coding=utf-8
import level

class Game(object):
    def __init__(self):
        self.level = level.Level()

    def render(self):
        self.level.render()


    def simulate(self, dt):
        self.level.simulate(dt)

    def on_mouse_motion(self, x, y, dx, dy):
        self.level.player.cursorPosX = x - self.level.player.WIDTH/2
