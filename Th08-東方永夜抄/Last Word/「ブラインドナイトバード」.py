# -*- coding: utf-8 -*-

veclist = []

way = 20
rot = Matrix3.RotationAxis(Vector3.UnitX, RAD * (180.0 / (way + 2)))
vec = Vector3.UnitY

for i in range(way):
	vec = vec * rot
	veclist.append(vec)

def world_task():
	for vec in veclist:
		for angle in [RAD, -RAD]:
			axis = vec ^ (vec ^ Vector3.UnitY)
			
			binder = [vec, Matrix3.RotationAxis(axis, angle * 12)]
			
			def shot_scale(task, axis = axis, binder = binder, color = (0x00A0A0 if angle < 0 else 0x0000A0)):
				shot = EntityShotStraight(WORLD, "SCALE", color)
				shot.Pos = CENTER_BONE.WorldPos
				shot.Velocity = binder[0] * (10.0 + (binder[0] * Vector3.UnitZ) + task.ExecutedCount * 0.08)
				shot.Upward = axis
				shot.LifeSpan = 180
				shot.Spawn()
				
				binder[0] = binder[0] * binder[1]
			WORLD.AddTask(shot_scale, 1, 120, 0, True)
WORLD.AddTask(world_task, 160, 4, 0)

def shot_s():
	for speed in [6, 8]:
		mat = Matrix3.RotationAxis(randomvec(), RAD * 30)
		
		for vec in objvertices("ico.obj", 2):
			shot = EntityShotStraight(WORLD, "S", 0x00A000)
			shot.Pos = CENTER_BONE.WorldPos
			shot.Velocity = vec * speed * mat
			shot.LifeSpan = 120
			shot.Spawn()
WORLD.AddTask(shot_s, 8, 60, 60)
