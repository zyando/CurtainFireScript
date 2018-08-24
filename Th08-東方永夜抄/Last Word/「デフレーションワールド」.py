# -*- coding: utf-8 -*-

veclist = objvertices("ico.obj", 1)

num_clone = 25
pause_frame = 56
move_frame = 110

pauseList = []

TARGET_BONE = EntityShot(WORLD, "BONE", 0)
TARGET_BONE.Pos = Vector3(300, 300, 400)
TARGET_BONE.Velocity = Vector3(-20, -20, 0)
TARGET_BONE.Spawn()

def world_task_func():
	cloneList = []

	def shot_knife1(way = 5):
		vec = randomvec()
		mat = Matrix3.RotationAxis(cross2(vec, randomvec()), RAD * 20)
		vec = vec * (mat * mat)
		mat = ~mat

		for i in range(way):
			for j in range(2):
				shot = EntityShot(WORLD, "KNIFE", 0xFFD700)
				shot.Velocity = vec * (1 + j * 0.5)
				shot.Pos = CENTER_BONE.WorldPos + shot.Velocity
				shot.LifeSpan = 600
				shot.Spawn()

				pauseList.append(shot)
			vec = vec * mat
	WORLD.AddTask(shot_knife1, 0, 1, 10)

	def shot_knife2(angle, axis):
		for vec in veclist:
			vec = vec
			mat = Matrix3.RotationAxis(cross2(vec, axis), angle)
			
			shot = EntityShot(WORLD, "KNIFE", 0x0000A0)
			shot.Velocity = vec * 4.0
			shot.Pos = CENTER_BONE.WorldPos + shot.Velocity
			shot.LifeSpan = 200
			shot.SetMotionInterpolationCurve(Vector2(0.3, 0.7), Vector2(0.3, 0.7), 30)

			def shot_task_func(shot = shot, mat = mat):
				shot.Velocity = shot.Velocity * mat * 0.5
			shot.AddTask(shot_task_func, 0, 1, 30)
			shot.Spawn()

			cloneList.append(shot)
			pauseList.append(shot)
	WORLD.AddTask(lambda: shot_knife2(RAD * 60, Vector3.UnitZ), 0, 1, 0)
	WORLD.AddTask(lambda: shot_knife2(-RAD * 60, Vector3.UnitZ), 0, 1, 0)
	WORLD.AddTask(lambda: shot_knife2(RAD * 60, Vector3.UnitX), 0, 1, 5)
	WORLD.AddTask(lambda: shot_knife2(-RAD * 60, Vector3.UnitX), 0, 1, 5)

	def shot_knife3():
		shot = EntityShot(WORLD, "KNIFE", 0x0000A0)
		shot.Pos = CENTER_BONE.WorldPos
		shot.Velocity = normalize(TARGET_BONE.WorldPos - shot.Pos) * 2.0
		shot.LifeSpan = 200
		shot.Spawn()

		cloneList.append(shot)
		pauseList.append(shot)
	WORLD.AddTask(shot_knife3, 3, 12, 10)

	get_waiting_frame = lambda frame = WORLD.FrameCount + move_frame: frame - WORLD.FrameCount

	def pause():
		for shot in pauseList:
			shot.Velocity = Vector3.Zero

			def move(shot = shot):
				shot.Velocity = shot.LookAtVec
			shot.AddTask(move, 0, 1, get_waiting_frame())
	WORLD.AddTask(pause, 0, 1, pause_frame)

	def clone(task):
		for src in cloneList:
			interval = normalize(src.LookAtVec) * 16

			shot = EntityShot(WORLD, "KNIFE", 0xA0A0A0)
			shot.LookAtVec = src.LookAtVec
			shot.Pos = src.Pos + interval * (-num_clone / 3 + task.ExecutedCount)
			shot.LifeSpan = 120

			def move(shot = shot):
				shot.Velocity = normalize(shot.LookAtVec) * 8.0
			shot.AddTask(move, 0, 1, get_waiting_frame())
			shot.Spawn()
	WORLD.AddTask(clone, 0, num_clone, 60, True)
WORLD.AddTask(world_task_func, 120, 2, 0)
