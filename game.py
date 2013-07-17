# coding=utf-8
import level
import pyglet
import gameEngine

class Game(object):
    def __init__(self):
        self.level = level.Level()
        self.camera = Camera()

    def render(self):
        self.level.render()


    def simulate(self, dt):
        self.level.simulate(dt)

    def on_mouse_motion(self, x, y, dx, dy):
        self.level.player.cursorPosX = x - self.level.player.WIDTH/2

class Camera(object):

    def __init__(self):
        self.x = 0
        self.y = 0

    def setPos(self, x, y):
        self.x = x
        self.y = y

        pyglet.gl.glLoadIdentity()
        pyglet.gl.glTranslated(0, gameEngine.GameEngine.W_HEIGHT / 2 + y, 0)
