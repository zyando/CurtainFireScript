# -*- coding: utf-8 -*-

veclist = []

way = 60
rot = Matrix3.RotationAxis(Vector3.UnitX, RAD * (180.0 / (way + 2)))
vec = Vector3.UnitY

for i in range(way):
	vec = vec * rot
	veclist.append(vec)

def world_task(task):
	for vec in veclist:
		for angle in [RAD, -RAD]:
			axis = vec ^ (vec ^ Vector3.UnitY)
			
			frame = Frame(vec, Matrix3.RotationAxis(axis, angle * 12))
			
			def shot_knife(task, parent = parent, axis = axis, frame = frame):
				shot = EntityShot(WORLD, "KNIFE", 0xA00000)
				shot.Pos = CENTER_BONE.WorldPos
				shot.Velocity = frame.vec * (4.0 + (frame.vec * Vector3.UnitZ) * 1 + task.ExecutedCount * 0.03)
				shot.Upward = axis
				shot.LivingLimit = 120
				shot()
				
				frame.vec = frame.vec * frame.rot
			WORLD.AddTask(shot_knife, 1, 120, 0, True)
			
			if (angle > 0 if task.ExecutedCount % 2 == 0 else angle < 0):
				def shot_l(frame = frame):
					shot = EntityShot(WORLD, "L", 0xFF0000)
					shot.Pos = CENTER_BONE.WorldPos
					shot.Velocity = parent.Pos * 2.0
					shot.LivingLimit = 160
					shot()
				WORLD.AddTask(shot_l, 3, 8, 4)
WORLD.AddTask(world_task, 160, 2, 0, True)