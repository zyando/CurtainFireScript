# -*- coding: utf-8 -*-
from CurtainFireMakerPlugin.Entities import *
from VecMath import *
from vectorutil import *
from randomutil import uniform
import math

veclist = []
objvertices("ico_tru2.obj", lambda v: veclist.append(+v))

def WORLD_task(task):
	for vec in veclist:
		for i in range(5):
			shot = EntityShot(WORLD, AMULET, 0xFFFFFF)
			shot.Velocity = vec * 3 * (1 + i * 0.6)
			shot.LivingLimit = 200
			shot()

	def shot_red_amulet():
		for i in range(144 + 16 * task.RunCount):
			shot = EntityShot(WORLD, AMULET, 0xA00000)
			shot.Velocity = randomvec() * uniform(1, 8)
			shot.Upward = randomvec()
			shot.LivingLimit = 200
			shot()
	WORLD.AddTask(shot_red_amulet, 1, 5, 0)

	def shot_M():
		for i in range(112):
			shot = EntityShot(WORLD, M, 0xA00000)
			shot.Velocity = randomvec() * uniform(1, 8)
			shot.Upward = randomvec()
			shot.LivingLimit = 200
			shot()
	WORLD.AddTask(shot_M, 1, 5, 0)
WORLD.AddTask(WORLD_task, 90, 4, 0, True)
