# -*- coding: utf-8 -*-

veclist = []

way = 45
rot = Matrix3.RotationX(RAD * (180.0 / (way + 1)))
vec = Vector3.UnitY

for i in range(way):
	vec = vec * rot
	veclist.append(vec)

def world_task(task):
	for vec in veclist:
		for angle in [RAD, -RAD]:
			axis = cross2(vec, Vector3.UnitY)
			binder = [vec]

			def shot_knife(task, binder = binder, rot = Matrix3.RotationAxis(axis, angle * 15, False), axis = axis):
				shot = EntityShotStraight(WORLD, "KNIFE", 0xA00000)
				shot.Velocity = binder[0] * (6.0 + dot(binder[0], Vector3.UnitZ) * 2 + task.ExecutedCount * 0.08)
				shot.Upward = axis
				shot.LifeSpan = 160
				shot.Spawn()
				
				binder[0] *= rot
			WORLD.AddTask(shot_knife, 0, 120, 0, True)
			
			if (angle > 0 if task.ExecutedCount % 2 == 0 else angle < 0):
				def shot_l(binder = binder):
					shot = EntityShotStraight(WORLD, "L", 0xFF0000, 0.6)
					shot.Velocity = binder[0] * 4.0
					shot.LifeSpan = 320
					shot.Spawn()
				WORLD.AddTask(shot_l, 3, 8, 4)
WORLD.AddTask(world_task, 160, 2, 0, True)