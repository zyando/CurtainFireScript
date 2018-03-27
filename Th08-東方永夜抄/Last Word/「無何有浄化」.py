# -*- coding: utf-8 -*-

veclist = objvertices("ico.obj", 2)

for vec in veclist:
	for angle in [RAD, -RAD]:
		for axis in [Vector3.UnitX, Vector3.UnitZ]:
			axis = vec ^ (vec ^ axis)
			parent = Entity(WORLD)
			
			rotPosMat = Matrix3.RotationAxis(axis, angle * 6)
			parent.Pos = vec
			
			def rotate(parent = parent, rotPosMat = rotPosMat, angle = angle):
				parent.Rot = Quaternion.Identity
				rotQuat = Quaternion.RotationAxis(axis, -angle * 4)
				
				def shot_dia():
					parent.Pos = parent.Pos * rotPosMat
					parent.Rot = parent.Rot * rotQuat
					
					shot = EntityShot(WORLD, "DIA", 0xA00050 if angle < 0 else 0x5000A0)
					shot.Pos = CENTER_BONE.WorldPos + parent.Pos * 640
					shot.Velocity = parent.Pos * parent.Rot * -2
					shot.LivingLimit = 120
					shot()
				parent.AddTask(shot_dia, 4, 8, 0)
			parent.AddTask(rotate, 32, 20, 0)
			parent()

def world_task():
	def shot_l(task):
		vec = +(TARGET_BONE.WorldPos - CENTER_BONE.WorldPos)
		axis = vec ^ (vec ^ Vector3.UnitY)
		
		angle = (task.ExecutedCount - 1) * RAD * 5 * 0.5
		mat1 = Matrix3.RotationAxis(axis, -RAD * 5)
		mat2 = Matrix3.RotationAxis(axis, angle)
		
		for i in range(task.ExecutedCount):
			shot = EntityShot(WORLD, "L", 0x4000D0)
			shot.Pos = CENTER_BONE.WorldPos
			shot.Velocity = vec * mat2 * 2.5
			shot()
			
			mat2 = mat2 * mat1
	WORLD.AddTask(shot_l, 5, 4, 0, True)
WORLD.AddTask(world_task, 90, 8, 90)