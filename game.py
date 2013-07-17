# coding=utf-8
import level
import pyglet
import gameEngine


class Game(object):
    def __init__(self):
        self.level = level.Level()
        self.camera = Camera()

        self.scoreTextShadow = pyglet.text.Label("WTF", x=11, y=gameEngine.GameEngine.W_HEIGHT - 1, anchor_y="top", bold=True, font_size=25, color=(0,0,0,255))
        self.scoreText = pyglet.text.Label("WTF", x=10, y=gameEngine.GameEngine.W_HEIGHT/2, anchor_y="top", bold=True, font_size=25)

        self.gameOverText = pyglet.text.Label("-~== GAME OVER ==~-", x=gameEngine.GameEngine.W_WIDTH/2, y=gameEngine.GameEngine.W_HEIGHT - 200, anchor_x="center", anchor_y="top", bold=True, font_size=40)
        self.gameOverScore = pyglet.text.Label("0000", x=gameEngine.GameEngine.W_WIDTH/2, y=gameEngine.GameEngine.W_HEIGHT/2, anchor_x="center", anchor_y="center", bold=True, font_size=35)

    def render(self):

        if not self.level.player.isDead:
            self.level.render()
            self.scoreTextShadow.text = str(int(self.level.score))
            self.scoreText.text = str(int(self.level.score))
            self.scoreTextShadow.y = - self.camera.y + gameEngine.GameEngine.W_HEIGHT - 1
            self.scoreText.y = - self.camera.y + gameEngine.GameEngine.W_HEIGHT
            self.scoreTextShadow.draw()
            self.scoreText.draw()

        else:
            self.camera.forcePos(0)

            self.gameOverText.draw()

            self.gameOverScore.text = str(int(self.level.score))
            self.gameOverScore.draw()

    def simulate(self, dt):
        if not self.level.player.isDead:
            self.camera.setPos(-self.level.player.startJumpY + gameEngine.GameEngine.W_HEIGHT/10)
            self.level.simulate(dt)
            self.camera.simulate(dt)

            if self.level.player.y < -self.camera.y:
                self.level.player.isDead = True

    def on_mouse_motion(self, x, y, dx, dy):
        self.level.player.cursorPosX += dx

    def on_key_press(self, key, modifiers):
        if key == pyglet.window.key.R and self.level.player.isDead:
            self.level = level.Level()


class Camera(object):

    def __init__(self):
        self.y = 0
        self.targetY = 0

    def setPos(self, y):
        if y < self.targetY:
            self.targetY = y

    def forcePos(self, y):
        self.y = y
        self.targetY = y
        pyglet.gl.glLoadIdentity()
        pyglet.gl.glTranslated(0, self.y, 0)

    def simulate(self, dt):
        self.y += (self.targetY - self.y) * dt * 2.5
        pyglet.gl.glLoadIdentity()
        pyglet.gl.glTranslated(0, self.y, 0)
