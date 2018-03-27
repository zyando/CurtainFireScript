# -*- coding: utf-8 -*-

veclist0 = objvertices("ico.obj", 0)
veclist1 = objvertices("ico.obj", 1)

def task_to_shoot_while_rotating(vec, axis, shottype, color, init_angle, angle_interval, speed, livinglimit):
	if abs(vec * axis) > 0.995 > 0: return lambda: 0

	axis = vec ^ (vec ^ axis)

	binder = Entity(WORLD)
	binder.vec = vec * Matrix3.RotationAxis(axis, init_angle)

	def shot_dia(rot = Matrix3.RotationAxis(axis, angle_interval)):
		shot = EntityShot(WORLD, shottype, color)
		shot.Pos = CENTER_BONE.WorldPos
		shot.Velocity = binder.vec * speed
		shot.LivingLimit = livinglimit
		shot()

		binder.vec *= rot
	return shot_dia

for vec in veclist0:
	for axis in Vector3.UnitX, Vector3.UnitZ:
		for i in range(4):
			WORLD.AddTask(task_to_shoot_while_rotating(vec, axis, "DIA", 0xA00000, RAD * i * 20, RAD * 4, 1 + i * 0.5, (4 - i) * 100), 2, 210, 60)

def task_to_shoot_mgc():
	mat = Matrix3.RotationAxis(randomvec(), RAD * random() * 90)

	for vec in veclist1:
		mgc = EntityShot(WORLD, "MAGIC_CIRCLE", 0xFFFFFF)
		mgc.Pos = HAND_BONE.WorldPos
		mgc.Velocity = vec * 4 * mat
		mgc.LivingLimit = 150

		def shot_s(mgc = mgc):
			shot = EntityShot(WORLD, "S", 0x0000A0)
			shot.Pos = mgc.Pos + randomvec() * (random() * 50)
			shot.LivingLimit = 120
			shot()
		mgc.AddTask(shot_s, 0, 120, 0)
		mgc()
WORLD.AddTask(task_to_shoot_mgc, 180, 3, 2)
