# -*- coding: utf-8 -*-

veclist0 = objvertices("ico.obj", 1)
veclist2 = objvertices("ico.obj", 2)

def task_to_shoot_while_rotating(vec, axis, shottype, color, speed, lifespan):
	if abs(vec * axis) > 0.995 > 0: return lambda: 0

	axis = vec ^ (vec ^ axis)
	rot = Matrix3.RotationAxis(axis, RAD * 5)
	binder = [vec]

	def shot_func():
		parent = EntityShot(WORLD, "BONE", 0xFFFFFF)
		parent.Velocity = binder[0] * speed
		parent.GetRecordedRot = lambda e: e.Rot
		parent.LifeSpan = lifespan
		parent()

		shot = EntityShot(WORLD, shottype, color, parent)
		shot.Velocity = binder[0] * speed
		shot.LifeSpan = lifespan
		shot()

		def rotate(rot = Quaternion.RotationAxis(axis, RAD * -150)):
			parent.Rot *= rot
			parent.Velocity *= 0
		parent.AddTask(rotate, 0, 1, 120)

		binder[0] *= rot
	return shot_func

for vec in veclist0:
	for axis, color in (Vector3.UnitZ, 0x0000A0), (-Vector3.UnitZ, 0x00A000), (Vector3.UnitX, 0x0000A0), (-Vector3.UnitX, 0x00A000):
		WORLD.AddTask(task_to_shoot_while_rotating(vec, axis, "RICE_M", color, 3.0, 720), 4, 80, 0)

def shot_dia():
	for vec in veclist2:
		shot = EntityShot(WORLD, "DIA_BRIGHT", 0x004040)
		shot.Velocity = vec * 3.0
		shot.LifeSpan = 800
		shot()
WORLD.AddTask(shot_dia, 15, 22, 0)
