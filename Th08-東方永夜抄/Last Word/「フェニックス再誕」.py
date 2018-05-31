# -*- coding: utf-8 -*-

poslist = [
	Vector3(8, 0, 2), Vector3(16, 0, 8), Vector3(24, 0, 14), Vector3(32, 0, 20),
	Vector3(26, 0, 20), Vector3(34, 0, 27), Vector3(42, 0, 34), Vector3(50, 0, 41),
	Vector3(28, 0, 25), Vector3(36, 0, 32)
	]

def shot_phenix():
	for pos in [pos * Matrix3(i, 1, 1) for i in [1, -1] for pos in poslist]:
		shot = EntityShot(WORLD, "S", 0xFF0000)
		shot.Pos = pos
		shot.Velocity = Vector3.UnitZ * -8
		shot()
	
	shot = EntityShot(WORLD, "L", 0xFF0000)
	shot.Pos = Vector3(0, 0, -8)
	shot.Velocity = Vector3.UnitZ * -8
	shot()
	
	shot = EntityShot(WORLD, "M", 0xFF0000)
	shot.Pos = Vector3(0, 0, 0)
	shot.Velocity = Vector3.UnitZ * -8
	shot()
WORLD.AddTask(shot_phenix, 5, 8, 60)

def shot_dia():
	for speed in 4, 6:
		mat = Matrix3.RotationAxis(randomvec(), RAD * 30)
		
		for vec in objvertices("ico.obj", 2):
			shot = EntityShotStraight(WORLD, "DIA", 0xFF0000)
			shot.Velocity = vec * mat * speed
			shot.LivingLimit = 200
			shot()
WORLD.AddTask(shot_dia, 10, 12, 0)
