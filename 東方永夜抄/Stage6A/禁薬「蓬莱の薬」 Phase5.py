# -*- coding: utf-8 -*-

veclists = [objvertices("ico.obj", i) for i in range(5)]

phase_start_frame = 4367
phase_finish_frame = 7271
phase_length = phase_finish_frame - phase_start_frame

WORLD.FrameCount = phase_start_frame - 322
WORLD.MaxFrame = phase_length

def get_acceleration(interval, length): return -(interval * interval) / (length * 2.0)

def phase5():
	interval = 100
	acceleration = get_acceleration(interval, phase_length - 500)

	print acceleration

	def shot_dia1(task):
		mat = Matrix3.RotationAxis(randomvec(), RAD * 30)

		for vec in veclists[3]:
			shot = EntityShot(WORLD, "DIA", 0x000040)
			shot.ModelData.Materials[0].Shininess = 130
			shot.Velocity = vec * mat * 2
			shot.LivingLimit = 400
			shot()
		task.Interval += int(acceleration)
		task.Interval = max(task.Interval, 5)
	WORLD.AddTask(shot_dia1, interval, interval / -acceleration + 8, 0, True)

	def shot_dia2():
		mat = Matrix3.RotationAxis(randomvec(), RAD * 30)

		for vec in veclists[1]:
			shot = EntityShot(WORLD, "DIA", 0x000040)
			shot.ModelData.Materials[0].Shininess = 130
			shot.Velocity = vec * mat * (2.0 if vec in veclists[1] else 4.0)
			shot.LivingLimit = 60 if vec in veclists[1] else 30

			def replace(orgn = shot):
				shot = EntityShot(WORLD, "DIA", 0x0000A0)
				shot.Pos = orgn.Pos
				shot.Velocity = orgn.Velocity
				shot.LivingLimit = orgn.LivingLimit * 8
				shot()
			shot.AddTask(replace, 0, 1, shot.LivingLimit)
			shot()
	WORLD.AddTask(shot_dia2, 10, phase_length / 10, 0)
WORLD.AddTask(phase5, 0, 1, 0)
