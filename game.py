# coding=utf-8
import level
import pyglet
import gameEngine


class Game(object):
    def __init__(self):
        self.level = level.Level()
        self.camera = Camera()

        self.scoreSaved = False

        self.scoreTextShadow = pyglet.text.Label("WTF", x=11, y=gameEngine.GameEngine.W_HEIGHT - 1, anchor_y="top", bold=True, font_size=25, color=(0, 0, 0, 255))
        self.scoreText = pyglet.text.Label("WTF", x=10, y=gameEngine.GameEngine.W_HEIGHT / 2, anchor_y="top", bold=True, font_size=25)

        self.gameOverText = pyglet.text.Label("-~== GAME OVER ==~-", x=gameEngine.GameEngine.W_WIDTH / 2, y=gameEngine.GameEngine.W_HEIGHT - 200, anchor_x="center", anchor_y="top", bold=True, font_size=40)
        self.gameOverBest = pyglet.text.Label("0000", x=gameEngine.GameEngine.W_WIDTH / 2, y=gameEngine.GameEngine.W_HEIGHT / 2, anchor_x="center", anchor_y="center", bold=True, font_size=35)
        self.gameOverScore = pyglet.text.Label("0000", x=gameEngine.GameEngine.W_WIDTH / 2, y=gameEngine.GameEngine.W_HEIGHT / 2 - 80, anchor_x="center", anchor_y="center", bold=True, font_size=35, color=(115, 158, 235, 255))
        self.restartText = pyglet.text.Label("Press [R] or click to restart the game.", x=gameEngine.GameEngine.W_WIDTH / 2, y=gameEngine.GameEngine.W_HEIGHT / 2 - 160, anchor_x="center", anchor_y="center", bold=True, font_size=20)

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

            if self.scoreSaved is False:
                file = open("highscore", "r")
                # get best score
                scoreMax = 0
                for line in file:
                    if int(line) > scoreMax:
                        scoreMax = int(line)
                file.close()

                # save score
                file = open("highscore", "a")
                file.write(str(int(self.level.score)) + "\n")
                self.scoreSaved = True
                file.close()

                if scoreMax != 0 and scoreMax > int(self.level.score):
                    self.gameOverBest.text = "Best Score: " + str(scoreMax)
                else:
                    self.gameOverBest.text = "* NEW RECORD *"

            self.gameOverScore.text = str(int(self.level.score))

            self.gameOverBest.draw()
            self.gameOverScore.draw()
            self.restartText.draw()

    def simulate(self, dt):
        if not self.level.player.isDead:
            self.level.simulate(dt)

            if self.level.player.y < -self.camera.y:
                self.level.player.isDead = True

            if self.level.player.item is None:
                self.camera.setPos(-self.level.player.startJumpY + gameEngine.GameEngine.W_HEIGHT / 10)
                self.camera.simulate(dt)
            else:
                self.camera.setPos(-self.level.player.y)
                self.camera.simulate(dt)

    def on_mouse_motion(self, x, y, dx, dy):
        self.level.player.cursorPosX += dx

    def on_mouse_press(self, button, x, y, modifiers):
        if self.level.player.isDead:
            self.level = level.Level()
            self.scoreSaved = False
        self.level.player.isShooting = True

    def on_mouse_release(self, x, y, button, modifiers):
        self.level.player.isShooting = False

    def on_key_press(self, key, modifiers):
        if key == pyglet.window.key.R and self.level.player.isDead:
            self.level = level.Level()
            self.scoreSaved = False


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
        self.y += int((self.targetY - self.y) * dt * 2.5)
        pyglet.gl.glLoadIdentity()
        pyglet.gl.glTranslated(0, self.y, 0)
