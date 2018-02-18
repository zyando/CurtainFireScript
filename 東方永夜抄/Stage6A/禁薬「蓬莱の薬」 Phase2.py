# -*- coding: utf-8 -*-

veclists = [objvertices("ico.obj", i) for i in range(4)]

phase_start_frame = 1021
phase_finish_frame = 2413
phase_length = phase_finish_frame - phase_start_frame

WORLD.FrameCount = phase_start_frame - 322
WORLD.MaxFrame = phase_length

def phase2():
	binder = Entity(WORLD)
	def rotate(rot = Quaternion.RotationAxis(Vector3.UnitY, RAD * (270.0 / phase_length))): binder.Rot *= rot
	binder.AddTask(rotate, 0, phase_length, 0)
	binder()

	def shot_rice():
		for vec in veclists[2]:
			shot = EntityShot(WORLD, "RICE_M", 0xA00000, 4)
			shot.Velocity = vec * binder.Rot * 10
			shot.LivingLimit = 100
			shot()
	WORLD.AddTask(shot_rice, 5, phase_length / 5, 0)

	def shot_dia():
		for vec in veclists[3]:
			shot = EntityShot(WORLD, "DIA_BRIGHT", 0x400000)
			shot.Velocity = vec * binder.Rot * 10
			shot.LivingLimit = 100
			shot()
	WORLD.AddTask(shot_dia, 40, phase_length / 40, 0)

	def shot_dia_to_target(veclist = [v for v in veclists[1] if v.z < -0.8]):
		mat = Matrix3.LookAt(TARGET_BONE.WorldPos - OWNER_BONE.WorldPos, Vector3.UnitY)

		for vec in veclist:
			for i in range(3):
				shot = EntityShot(WORLD, "DIA_BRIGHT", 0x000040)
				shot.Velocity = vec * mat * (1 + i * 0.5) * 2
				shot.LivingLimit = 400
				shot()
	WORLD.AddTask(shot_dia_to_target, 5, (phase_length - 622) / 5, 622)
WORLD.AddTask(phase2, 0, 1, 0)
