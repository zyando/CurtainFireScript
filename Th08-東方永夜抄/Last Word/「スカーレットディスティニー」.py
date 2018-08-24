# -*- coding: utf-8 -*-

veclist = []

way = 40
rot = Matrix3.RotationAxis(Vector3.UnitX, RAD * (180.0 / (way + 2)))
vec = Vector3.UnitY

for i in range(way):
	vec = vec * rot
	veclist.append(vec)

def world_task(task):
	for vec in veclist:
		for angle in [RAD, -RAD]:
			axis = cross2(vec, Vector3.UnitY)
			
			binder = [vec, Matrix3.RotationAxis(axis, angle * 12)]
			
			def shot_knife(task, axis = axis, binder = binder):
				shot = EntityShotStraight(WORLD, "KNIFE", 0xA00000)
				shot.Pos = CENTER_BONE.WorldPos
				shot.Velocity = binder[0] * (10.0 + dot(binder[0], Vector3.UnitZ) + task.ExecutedCount * 0.08)
				shot.Upward = axis
				shot.LifeSpan = 180
				shot.Spawn()
				
				binder[0] = binder[0] * binder[1]
			WORLD.AddTask(shot_knife, 1, 120, 0, True)
			
			if (angle > 0 if task.ExecutedCount % 2 == 0 else angle < 0):
				def shot_l(binder = binder):
					shot = EntityShotStraight(WORLD, "L", 0xFF0000)
					shot.Pos = CENTER_BONE.WorldPos
					shot.Velocity = binder[0] * 5.0
					shot.LifeSpan = 240
					shot.Spawn()
				WORLD.AddTask(shot_l, 3, 8, 4)
WORLD.AddTask(world_task, 160, 4, 0, True)
