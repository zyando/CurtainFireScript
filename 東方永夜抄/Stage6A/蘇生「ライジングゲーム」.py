# -*- coding: utf-8 -*-

veclist = []
objvertices("ico.obj", lambda v: veclist.append(+v), 1)

def task_to_shoot_while_rotating(vec, axis, shottype, color, angle_interval, speed, livinglimit):
	if abs(vec * axis) > 0.995 > 0: return lambda: 0
	
	axis = vec ^ (vec ^ axis)
	rot = Matrix3.RotationAxis(axis, angle_interval)
	
	frame = Frame(vec, rot)
	
	def shot_dia():
		shot = EntityShot(WORLD, shottype, color)
		shot.Velocity = frame.vec * speed
		shot.LivingLimit = livinglimit
		shot()
		
		frame.vec *= frame.rot
	return shot_dia

for vec in veclist:
	for axis in Vector3.UnitX, Vector3.UnitZ:
		WORLD.AddTask(task_to_shoot_while_rotating(vec, axis, "DIA", 0x400000, RAD * 3, 4.0, 200), 2, 240, 0)
		WORLD.AddTask(task_to_shoot_while_rotating(vec, axis, "M", 0xA00000, RAD * -4, 4.0, 200), 6, 80, 0)
		WORLD.AddTask(task_to_shoot_while_rotating(vec, axis, "L", 0xA00000, RAD * 4, 6.0, 150), 10, 48, 0)


