# -*- coding: utf-8 -*-

veclists = [objvertices("ico.obj", i) for i in range(4)]

phase_start_frame = 467
phase_finish_frame = 1020
phase_length = phase_finish_frame - phase_start_frame

WORLD.FrameCount = phase_start_frame - 322
WORLD.MaxFrame = phase_length

def phase1():
	def shot_dia(task):
		mat = Matrix3.RotationAxis(randomvec(), RAD * 30)

		for vec in veclists[2]:
			shot = EntityShot(WORLD, "DIA_BRIGHT", 0x000040)
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
		task.Interval -= 1
		task.Interval = max(task.Interval, 5)
	WORLD.AddTask(shot_dia, 20, (phase_length - 110) / 5 + 15, 0, True)
WORLD.AddTask(phase1, 0, 1, 0)
