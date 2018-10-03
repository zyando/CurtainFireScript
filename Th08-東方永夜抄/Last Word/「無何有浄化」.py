# -*- coding: utf-8 -*-

veclist = objvertices("ico.obj", 1)

for vec in veclist:
	for angle in [RAD, -RAD]:
		for axis in [Vector3.UnitX, Vector3.UnitZ]:
			if abs(dot(vec, axis)) > 0.95: continue

			axis = cross3(vec, vec, axis)
			
			rotPosMat = Matrix3.RotationAxis(axis, angle * 6)
			binder = [vec, Quaternion.Identity]
			
			def rotate(binder = binder, rotPosMat = rotPosMat, angle = angle):
				binder[1] = Quaternion.Identity
				rotQuat = Quaternion.RotationAxis(axis, -angle * 4)
				
				def shot_dia():
					binder[0] *= rotPosMat
					binder[1] *= rotQuat
					
					shot = EntityShot(WORLD, "DIA", 0xA00050 if angle < 0 else 0x5000A0)
					shot.Pos = CENTER_BONE.WorldPos + binder[0] * 640
					shot.Velocity = binder[0] * binder[1] * -6
					shot.LifeSpan = 110
					shot.Spawn()
				WORLD.AddTask(shot_dia, 4, 8, 0)
			WORLD.AddTask(rotate, 32, 20, 0)

def world_task():
	def shot_l(task):
		vec = normalize(TARGET_BONE.WorldPos - CENTER_BONE.WorldPos)
		axis = cross2(vec, Vector3.UnitY)
		
		angle = (task.ExecutedCount - 1) * RAD * 5 * 0.5
		mat1 = Matrix3.RotationAxis(axis, -RAD * 5)
		mat2 = Matrix3.RotationAxis(axis, angle)
		
		for i in range(task.ExecutedCount):
			shot = EntityShot(WORLD, "L", 0x4000D0)
			shot.Pos = CENTER_BONE.WorldPos
			shot.Velocity = vec * mat2 * 12
			shot.Spawn()
			
			mat2 = mat2 * mat1
	WORLD.AddTask(shot_l, 5, 4, 0, True)
WORLD.AddTask(world_task, 90, 8, 90)
