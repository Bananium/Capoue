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
        self.camera.setPos( -self.level.player.startJumpY + gameEngine.GameEngine.W_HEIGHT/10 )
        self.level.simulate(dt)
        self.camera.simulate(dt)

    def on_mouse_motion(self, x, y, dx, dy):
        self.level.player.cursorPosX = x - self.level.player.WIDTH/2


class Camera(object):

    def __init__(self):
        self.y = 0
        self.targetY = 0

    def setPos(self, y):
        if y < self.targetY:
            self.targetY = y

    def simulate(self, dt):
        self.y += (self.targetY - self.y) * dt * 2.5
        pyglet.gl.glLoadIdentity()
        pyglet.gl.glTranslated(0, self.y, 0)
