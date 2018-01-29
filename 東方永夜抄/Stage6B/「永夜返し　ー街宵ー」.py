# -*- coding: utf-8 -*-

veclist = []
objvertices("ico.obj", lambda v: veclist.append(+v), 3)

def shot_dia():
	for vec in veclist:
		shot = EntityShot(WORLD, "DIA", 0xFFFFFF)
		shot.Velocity = vec * 1
		shot.LivingLimit = 400
		shot()
WORLD.AddTask(lambda: WORLD.AddTask(shot_dia, 10, 40, 0), 440, 2, 0)

def shot_m(task):
	shot = EntityShot(WORLD, "M", 0xA00000)
	shot.Velocity = Vector3.UnitX * (task.RunCount % 2 * 2 - 1) * 2
	shot.LivingLimit = 230
	
	def turn(): shot.Velocity = +(TARGET_BONE.WorldPos - shot.Pos) * 4
	shot.AddTask(turn, 0, 1, 30)
	
	shot()
WORLD.AddTask(shot_m, 6, 130, 90, True)
