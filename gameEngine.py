# coding=utf-8
import pyglet
import game


class GameEngine(pyglet.window.Window):
    W_WIDTH = 1024
    W_HEIGHT = 640

    def __init__(self):
        super(GameEngine, self).__init__(width=self.W_WIDTH, height=self.W_HEIGHT, resizable=False)
        self.game = game.Game()

        # - Options generales -
        self.set_vsync(False)
        self.set_caption(u"Capoué")

        # - Couleur de fond -
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glClearColor(0.5, 0.75, 1, 1)

        # - Physique -
        pyglet.clock.schedule_interval(lambda x: False, 1/100000000.0)  # Debridage complet des FPS
        pyglet.clock.schedule_interval(self.physicEngine, 1/100.0)

    def physicEngine(self, dt):
        self.game.simulate(dt)

    def on_mouse_motion(self, x, y, dx, dy):
        self.game.on_mouse_motion(x, y, dx, dy)

    def on_draw(self):
        self.clear()
        self.game.render()

    def start(self):
        pyglet.app.run()
