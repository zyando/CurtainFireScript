# -*- coding: utf-8 -*-
from random import uniform

veclist = []
objvertices("ico.obj", lambda v: veclist.append(+v), 2)

def world_task(task):
	for vec in veclist:
		for i in range(5):
			shot = EntityShot(WORLD, AMULET, 0xFFFFFF)
			shot.Pos = OWNER_BONE.WorldPos
			shot.Velocity = vec * 5 * (1 + i * 1)
			shot.LivingLimit = 200
			shot()

	def shot_red_amulet():
		for i in range(288 + 32 * task.RunCount):
			shot = EntityShot(WORLD, AMULET, 0xA00000)
			shot.Pos = OWNER_BONE.WorldPos
			shot.Velocity = randomvec() * uniform(4, 12)
			shot.Upward = randomvec()
			shot.LivingLimit = 200
			shot()
	WORLD.AddTask(shot_red_amulet, 1, 5, 0)

	def shot_M():
		for i in range(160):
			shot = EntityShot(WORLD, M, 0xA00000)
			shot.Pos = OWNER_BONE.WorldPos
			shot.Velocity = randomvec() * uniform(4, 12)
			shot.Upward = randomvec()
			shot.LivingLimit = 200
			shot()
	WORLD.AddTask(shot_M, 1, 5, 0)
WORLD.AddTask(world_task, 90, 4, 0, True)
