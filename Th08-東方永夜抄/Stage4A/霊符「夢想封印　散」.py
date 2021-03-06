# -*- coding: utf-8 -*-

veclist = objvertices("ico.obj", 2)

def world_task(task):
	for vec in veclist:
		for i in range(5):
			shot = EntityShot(WORLD, "AMULET", 0xFFFFFF)
			shot.Pos = CENTER_BONE.WorldPos
			shot.Velocity = vec * 5 * (1 + i * 1)
			shot.LifeSpan = 64 if shot.Velocity.Length() > 16 else 128
			shot.Spawn()

	def shot_red_amulet():
		for i in range(540 + 100 * task.ExecutedCount):
			shot = EntityShot(WORLD, "AMULET", 0xA00000)
			shot.Pos = CENTER_BONE.WorldPos
			shot.Velocity = randomvec() * uniform(8, 30)
			shot.Upward = randomvec()
			shot.LifeSpan = 64 if shot.Velocity.Length() > 16 else 128
			shot.Spawn()
	WORLD.AddTask(shot_red_amulet, 1, 5, 0)

	def shot_M():
		for i in range(300):
			shot = EntityShot(WORLD, "M", 0xA00000)
			shot.Pos = CENTER_BONE.WorldPos
			shot.Velocity = randomvec() * uniform(8, 30)
			shot.Upward = randomvec()
			shot.LifeSpan = 64 if shot.Velocity.Length() > 16 else 128
			shot.Spawn()
	WORLD.AddTask(shot_M, 1, 5, 0)
WORLD.AddTask(world_task, 65, 5, 0, True)