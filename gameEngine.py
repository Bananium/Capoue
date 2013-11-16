# -*- coding: utf-8 -*-
import pyglet
import game
import time


class GameEngine(pyglet.window.Window):
    W_WIDTH = 1024
    W_HEIGHT = 640

    def __init__(self):
        super(GameEngine, self).__init__(width=self.W_WIDTH, height=self.W_HEIGHT, resizable=False)
        self.game = game.Game()

        # - Options generales -
        self.set_vsync(True)
        self.set_caption(u"Capoué")

        self.set_mouse_visible(False)
        self.set_exclusive_mouse(True)

        # - Couleur de fond -
        pyglet.gl.glEnable(pyglet.gl.GL_BLEND)
        pyglet.gl.glClearColor(0.2, 0.2, 0.2, 1)

        # - Physique -
        pyglet.clock.schedule_interval(lambda x: False, 1 / 100000000.0)  # Debridage complet des FPS
        pyglet.clock.schedule_interval(self.physicEngine, 1 / 200000.0)

    def physicEngine(self, dt):
        self.game.simulate(dt)

    def on_mouse_motion(self, x, y, dx, dy):
        self.game.on_mouse_motion(x, y, dx, dy)

    def on_mouse_press(self, button, x, y, modifiers):
        self.game.on_mouse_press(button, x, y, modifiers)

    def on_mouse_release(self, x, y, button, modifiers):
        self.game.on_mouse_release(x, y, button, modifiers)

    def on_mouse_drag(self, x, y, dx, dy, button, modifiers):
        self.on_mouse_motion(x, y, dx, dy)
        self.on_mouse_press(button, x, y, modifiers)

    def on_key_press(self, key, modifiers):
        if key == pyglet.window.key.ESCAPE:
            self.close()
        else:
            self.game.on_key_press(key, modifiers)

    def on_draw(self):
        # start = time.time()
        self.clear()
        self.game.render()
        # print(1 / (time.time() - start))

    def start(self):
        pyglet.app.run()
