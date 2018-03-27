# -*- coding: utf-8 -*-

veclists = [objvertices("ico.obj", i) for i in range(4)]

def task_to_shoot_while_rotating(vec, axis, shottype, color, angle_interval, speed, livinglimit):
	if abs(vec * axis) > 0.995 > 0: return lambda: 0

	axis = vec ^ (vec ^ axis)

	binder = Entity(WORLD)
	binder.vec = vec

	def shot_dia(rot = Matrix3.RotationAxis(axis, angle_interval)):
		shot = EntityShot(WORLD, shottype, color)
		shot.Pos = CENTER_BONE.WorldPos
		shot.Velocity = binder.vec * speed
		shot.LivingLimit = livinglimit
		shot()

		binder.vec *= rot
	return shot_dia

for axis in Vector3.UnitX, Vector3.UnitY, Vector3.UnitZ:
    for vec in veclists[1]:
		WORLD.AddTask(task_to_shoot_while_rotating(vec, axis, "DIA_BRIGHT", 0x400000, RAD * 3, 4.0, 240), 2, 300, 0)
		WORLD.AddTask(task_to_shoot_while_rotating(vec, axis, "M", 0xA00000, RAD * -4, 4.0, 240), 6, 100, 0)

    for vec in veclists[0]:
		WORLD.AddTask(task_to_shoot_while_rotating(vec, axis, "L", 0xA00000, RAD * 4, 6.0, 180), 10, 60, 0)
