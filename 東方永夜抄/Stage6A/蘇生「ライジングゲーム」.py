# -*- coding: utf-8 -*-

veclist = []
objvertices("ico.obj", lambda v: veclist.append(+v), 1)

def task_to_shoot_while_rotating(vec, axis, shottype, color, specular, angle_interval, speed, livinglimit):
	if abs(vec * axis) > 0.995 > 0: return lambda: 0
	
	axis = vec ^ (vec ^ axis)
	
	binder = Entity(WORLD)
	binder.vec = vec
	
	def shot_dia(rot = Matrix3.RotationAxis(axis, angle_interval)):
		shot = EntityShot(WORLD, shottype, color)
		shot.Velocity = binder.vec * speed
		shot.LivingLimit = livinglimit
		shot.ModelData.Materials[0].Shininess = specular
		shot()
		
		binder.vec *= rot
	return shot_dia

for vec in veclist:
	for axis in Vector3.UnitX, Vector3.UnitZ:
		WORLD.AddTask(task_to_shoot_while_rotating(vec, axis, "DIA", 0x400000, 130, RAD * 3, 4.0, 240), 2, 480, 0)
		WORLD.AddTask(task_to_shoot_while_rotating(vec, axis, "M", 0xA00000, 108, RAD * -4, 4.0, 240), 6, 160, 0)
		WORLD.AddTask(task_to_shoot_while_rotating(vec, axis, "L", 0xA00000, 0, RAD * 4, 6.0, 180), 10, 96, 0)


