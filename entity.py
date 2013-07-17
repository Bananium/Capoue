# -*- encoding: UTF-8 -*-

import time
import gameEngine
from pyglet.gl import * # parce les pyglet.gl.GLMACHIN non merci

class Plateform(object):
	def __init__(self, x, y, width=20, height=20):
		self.x = x
		self.y = y
		self.width = width
		self.height = height

	def render():
		glBegin(GL_QUADS)
		glVertex2i(self.x, self.y)
		glVertex2i(self.x + self.width, self.y)
		glVertex2i(self.x + self.width, self.y + 20)
		glVertex2i(self.x, self.y + 20)
		glEnd()

class Player(object):

	WIDTH = 48
	HEIGHT = 48

	def __init__(self):
		self.x = 0
		self.y = 0

		self.dy = 0

		self.startJumpY = 0

	def move(self, cursorPosX):
		xBefore, yBefore = self.x, self.y
		
		# Deplacement en x
		dx = cursorPosX - self.x
		self.x = (self.x + dx) % gameEngine.GameEngine


		pass

	def render(self):
		glBegin(GL_QUADS)
		glVertex2i(self.x, self.y)
		glVertex2i(self.x + self.WIDTH, self.y)
		glVertex2i(self.x + self.WIDTH, self.y + self.HEIGHT)
		glVertex2i(self.x, self.y + self.HEIGHT)
		glEnd()


# 1/2 * g * t^2 + v0 * t + pos0
