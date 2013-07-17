import pyglet


class GameEngine(pyglet.window.Window):
    W_WIDTH = 1024
    W_HEIGHT = 640

    def __init__(self):
        super(GameEngine, self).__init__(width=self.W_WIDTH, height=self.W_HEIGHT, resizable=True)

    def start(self):
        pyglet.app.run()
