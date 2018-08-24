# -*- coding: utf-8 -*-

def shot_func(vec, axis):
	axis = vec ^ (vec ^ axis)
	
	binder = [vec * 20.0, vec * 20.0]
	
	mat0 = Matrix3.RotationAxis(axis, RAD * 16)
	mat1 = Matrix3.RotationAxis(axis, RAD * 80)
	mat2 = Matrix3.RotationAxis(axis, RAD * -6)
	matList = [mat0, mat1, mat2, mat2]
	
	def shot_task(task):
		def shot_s():
			binder[0] = binder[0] * matList[0]
			matList[2] = matList[3] *  matList[2]
			
			shot = EntityShot(WORLD, "S", 0xFFFFFF)
			shot.Pos = CENTER_BONE.WorldPos + binder[0]
			shot.Velocity = +binder[0] * 1.6
			shot.SetMotionInterpolationCurve(Vector2(0.2, 0.8), Vector2(0.2, 0.8), 60)
			shot.LifeSpan = 60
			shot.Spawn()
			
			def shot_butterfly():
				shot1 = EntityShot(WORLD, "BUTTERFLY", 0xA0A000)
				shot1.Pos = shot.Pos
				shot1.Velocity = +shot.Pos * 3.2
				shot1.LifeSpan = 200
				shot1()
				
				shot1 = EntityShot(WORLD, "BUTTERFLY", 0x00A000)
				shot1.Pos = shot.Pos
				shot1.Velocity = (+shot.Pos * 3.2) * matList[1]
				shot1.LifeSpan = 200
				shot1()
				
				if task.ExecutedCount == 1:
					shot1 = EntityShot(WORLD, "BUTTERFLY", 0x0000A0)
					shot1.Pos = shot.Pos
					shot1.Velocity = (+shot.Pos * 3.2) * (matList[1] ^ 2) * matList[2]
					shot1.LifeSpan = 200
					shot1()
			shot.AddTask(shot_butterfly, 0, 1, 60)
		WORLD.AddTask(shot_s, 5, 12, 0)
	WORLD.AddTask(shot_task, 130, 2, 0, True)
	
	mat0 = Matrix3.RotationAxis(axis, RAD * 16)
	
	def shot_task_func3(task):
		def shot_task_func4():
			binder[1] = binder[1] * (mat0 if task.ExecutedCount % 2 == 0 else ~mat0)
			
			shot = EntityShot(WORLD, "BUTTERFLY", 0x0000A0 if task.ExecutedCount % 2 == 0 else 0xA00000)
			shot.Pos = CENTER_BONE.WorldPos + binder[1]
			shot.Velocity = +binder[1] * 12
			shot.LifeSpan = 100
			shot.Spawn()
		WORLD.AddTask(shot_task_func4, 2, 20, 0)
	WORLD.AddTask(shot_task_func3, 40, 4, 90, True)

for vec in objvertices("ico.obj", 1):
	for axis in Vector3.UnitX, Vector3.UnitZ: 
		shot_func(vec, axis)
