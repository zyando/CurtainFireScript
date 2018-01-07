# -*- coding: utf-8 -*-

def shot_func(vec, axis):
	axis = vec ^ (vec ^ axis)
	
	parent1 = Entity(WORLD)
	parent1.Pos = vec * 20.0
	parent1()
	
	mat0 = Matrix3.RotationAxis(axis, RAD * 16)
	mat1 = Matrix3.RotationAxis(axis, RAD * 80)
	mat2 = Matrix3.RotationAxis(axis, RAD * -6)
	matList = [mat0, mat1, mat2, mat2]
	
	def shot_task(task, parent1 = parent1, matList = matList):
		def shot_s(task = task, parent1 = parent1, matList = matList):
			parent1.Pos = parent1.Pos * matList[0]
			matList[2] = matList[3] *  matList[2]
			
			shot = EntityShot(WORLD, "S", 0xFFFFFF)
			shot.Pos = OWNER_BONE.WorldPos + parent1.Pos
			shot.Velocity = +shot.Pos * 1.6
			shot.SetMotionInterpolationCurve(Vector2(0.2, 0.8), Vector2(0.2, 0.8), 60)
			shot.LivingLimit = 60
			shot()
			
			def shot_butterfly(shot = shot, matList = matList):
				shot1 = EntityShot(WORLD, "BUTTERFLY", 0xA0A000)
				shot1.Pos = shot.Pos
				shot1.Velocity = +shot.Pos * 3.2
				shot1.LivingLimit = 200
				shot1()
				
				shot1 = EntityShot(WORLD, "BUTTERFLY", 0x00A000)
				shot1.Pos = shot.Pos
				shot1.Velocity = (+shot.Pos * 3.2) *matList[1]
				shot1.LivingLimit = 200
				shot1()
				
				if task.RunCount == 1:
					shot1 = EntityShot(WORLD, "BUTTERFLY", 0x0000A0)
					shot1.Pos = shot.Pos
					shot1.Velocity = (+shot.Pos * 3.2) * (matList[1] ^ 2) * matList[2]
					shot1.LivingLimit = 200
					shot1()
			shot.AddTask(shot_butterfly, 0, 1, 60)
		parent1.AddTask(shot_s, 5, 12, 0)
	parent1.AddTask(shot_task, 130, 2, 0, True)
	
	parent2 = Entity(WORLD)
	parent2.Pos = vec * 20.0
	parent2()
	
	mat0 = Matrix3.RotationAxis(axis, RAD * 16)
	
	def shot_task_func3(task, parent2 = parent2, mat0 = mat0):
		def shot_task_func4(task = task, parent2 = parent2, mat0 = mat0):
			parent2.Pos = parent2.Pos * (mat0 if task.RunCount % 2 == 0 else ~mat0)
			
			shot = EntityShot(WORLD, "BUTTERFLY", 0x0000A0 if task.RunCount % 2 == 0 else 0xA00000)
			shot.Pos = OWNER_BONE.WorldPos + parent2.Pos
			shot.Velocity = +parent2.Pos * 9
			shot.LivingLimit = 100
			shot()
		parent2.AddTask(shot_task_func4, 2, 20, 0)
	parent2.AddTask(shot_task_func3, 40, 4, 90, True)
vecList = []
objvertices("ico.obj", lambda v: vecList.append(v), 1)
for vec in vecList:
	for axis in Vector3.UnitX, Vector3.UnitZ: 
		shot_func(vec, axis)