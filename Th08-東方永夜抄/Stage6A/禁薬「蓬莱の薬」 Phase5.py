# -*- coding: utf-8 -*-

veclists = [objvertices("ico.obj", i) for i in range(5)]

#phase_start_frame = 4367 + WORLD.FrameCount
#phase_finish_frame = 7271
phase_start_frame = 2280
phase_finish_frame = 3000
phase_length = phase_finish_frame - phase_start_frame

WORLD.FrameCount = phase_start_frame #- 322
WORLD.MaxFrame = phase_length + 300

def get_acceleration(interval, length): return -(interval * interval) / (length * 2.0)

def phase5():
	interval = 100
	acceleration = get_acceleration(interval, phase_length)

	print acceleration

	def shot_dia1():
		mat = Matrix3.RotationAxis(randomvec(), RAD * 30)

		for vec in veclists[3]:
			shot = EntityShotStraight(WORLD, "DIA_BRIGHT", 0x000040)
			shot.Velocity = vec * mat * 2
			shot.LivingLimit = 400
			shot()
	WORLD.AddTask(shot_dia1, lambda i: max(5, interval + int(acceleration * i)), interval / -acceleration + 8, 0)

	def shot_dia2():
		mat = Matrix3.RotationAxis(randomvec(), RAD * 30)

		for vec in veclists[1]:
			shot = EntityShotStraight(WORLD, "DIA_BRIGHT", 0x000040)
			shot.Velocity = vec * mat * (2.0 if vec in veclists[1] else 4.0)
			shot.LivingLimit = 60 if vec in veclists[1] else 30

			def replace(orgn = shot):
				shot = EntityShotStraight(WORLD, "DIA", 0x0000A0)
				shot.Pos = orgn.Pos
				shot.Velocity = orgn.Velocity
				shot.LivingLimit = orgn.LivingLimit * 8
				shot()
			WORLD.AddTask(replace, 0, 1, shot.LivingLimit)
			shot()
	WORLD.AddTask(shot_dia2, 10, phase_length / 10, 0)
WORLD.AddTask(phase5, 0, 1, 0)
