# -*- coding: utf-8 -*-

veclists = [objvertices("ico.obj", i) for i in range(3)]

phase_start_frame = 2414
phase_finish_frame = 3427 - 120
phase_length = phase_finish_frame - phase_start_frame

WORLD.FrameCount = phase_start_frame - 322
WORLD.MaxFrame = phase_length + 400

def phase3():
	def shot_dia():
		mat = Matrix3.RotationAxis(randomvec(), RAD * 30)

		for vec in veclists[2]:
			shot = EntityShot(WORLD, "DIA_BRIGHT", 0x400000)
			shot.Velocity = vec * mat * 2
			shot.LivingLimit = 60

			def replace(orgn = shot):
				for i in range(2):
					shot = EntityShot(WORLD, "DIA", 0xA00000)
					shot.Pos = orgn.Pos
					shot.Velocity = +orgn.Velocity * (4.0 if i == 0 else -2.0)
					shot.LivingLimit = 200 if i == 0 else 460
					shot()
			shot.AddTask(replace, 0, 1, shot.LivingLimit)
			shot()
	WORLD.AddTask(shot_dia, 20, phase_length / 20, 0)
WORLD.AddTask(phase3, 0, 1, 0)
