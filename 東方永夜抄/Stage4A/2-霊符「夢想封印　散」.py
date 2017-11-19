# -*- coding: utf-8 -*-
from CurtainFireMakerPlugin.Entities import *

from VecMath import *
from vectorutil import *
from randomutil import uniform, randint
import math

world.ModelName = u"夢符「夢想封印　散」"

RAD = math.pi / 180.0

veclist = []
objvertices("ico_tru1.obj", lambda v: veclist.append(+v))
objvertices("snub_cube.obj", lambda v: veclist.append(+v))

def world_task():
	for vec in veclist:
		for i in range(5):
			shot = EntityShot(world, "AMULET", 0xFFFFFF)
			shot.Velocity = vec * 2 * (1 + i * 0.4)
			shot.LivingLimit = 200
			shot()
	
	def shot_red_amulet():
		for i in range(40):
			shot = EntityShot(world, "AMULET", 0xA00000)
			shot.Velocity = randomvec() * uniform(1, 6)
			shot.Upward = randomvec()
			shot.LivingLimit = 200
			shot()
	world.AddTask(shot_red_amulet, 1, 5, 0)
	
	def shot_M():
		for i in range(20):
			shot = EntityShot(world, "M", 0xA00000)
			shot.Velocity = randomvec() * uniform(1, 6)
			shot.Upward = randomvec()
			shot.LivingLimit = 200
			shot()
	world.AddTask(shot_M, 1, 5, 0)
world.AddTask(world_task, 90, 4, 0)