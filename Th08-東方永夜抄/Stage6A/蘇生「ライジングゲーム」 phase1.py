# -*- coding: utf-8 -*-

veclists = [objvertices("ico.obj", i) for i in range(2)]

def task_to_shoot_while_rotating(vec, axis, shottype, color, angle_interval, speed, lifespan):
	if abs(vec * axis) > 0.995 > 0: return lambda: 0

	axis = cross3(vec, vec, axis)

	binder = [vec]

	def shot_dia(rot = Matrix3.RotationAxis(axis, angle_interval)):
		shot = EntityShotStraight(WORLD, shottype, color)
		shot.Pos = CENTER_BONE.WorldPos
		shot.Velocity = binder[0] * speed
		shot.LifeSpan = lifespan
		shot.Spawn()

		binder[0] *= rot
	return shot_dia

def compress(func, veclist):
	funclist = [func(vec, axis) for axis in Vector3.Units for vec in veclist]
	return lambda: [f() for f in funclist]

WORLD.AddTask(compress(lambda v, a: task_to_shoot_while_rotating(v, a, "DIA_BRIGHT", 0x400000, RAD * 3, 4.0, 240), veclists[1]), 2, 300, 0)
WORLD.AddTask(compress(lambda v, a: task_to_shoot_while_rotating(v, a, "M", 0xA00000, RAD * -4, 4.0, 240), veclists[1]), 6, 100, 0)
WORLD.AddTask(compress(lambda v, a: task_to_shoot_while_rotating(v, a, "L", 0xA00000, RAD * 4, 6.0, 180), veclists[0]), 10, 60, 0)
