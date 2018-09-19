# -*- coding: utf-8 -*-

poslist = [
	Vector3(12, 0, 4), Vector3(24, 0, 12), Vector3(36, 0, 21), Vector3(48, 0, 30),
	Vector3(39, 0, 30), Vector3(51, 0, 39), Vector3(63, 0, 51), Vector3(75, 0, 61),
	Vector3(42, 0, 37), Vector3(54, 0, 48)
	]

def shot_phenix():
	for pos in [pos * Matrix3(i, 1, 1) for i in [1, -1] for pos in poslist]:
		shot = EntityShot(WORLD, "S", 0xFF0000, 2)
		shot.Pos = pos
		shot.Velocity = Vector3.UnitZ * -12
		shot.Spawn()
	
	shot = EntityShot(WORLD, "L", 0xFF0000)
	shot.Pos = Vector3(0, 0, -8)
	shot.Velocity = Vector3.UnitZ * -12
	shot.Spawn()
	
	shot = EntityShot(WORLD, "M", 0xFF0000)
	shot.Pos = Vector3(0, 0, 0)
	shot.Velocity = Vector3.UnitZ * -12
	shot.Spawn()
WORLD.AddTask(shot_phenix, 5, 8, 60)

def shot_dia():
	for speed in 4, 6:
		mat = Matrix3.RotationAxis(randomvec(), RAD * 30)
		
		for vec in objvertices("ico.obj", 2):
			shot = EntityShotStraight(WORLD, "DIA", 0xFF0000)
			shot.Velocity = vec * mat * speed
			shot.LifeSpan = 200
			shot.Spawn()
WORLD.AddTask(shot_dia, 10, 12, 0)
