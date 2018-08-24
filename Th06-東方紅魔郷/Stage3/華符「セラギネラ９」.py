# -*- coding: utf-8 -*-

veclist0 = objvertices("ico.obj", 0)
veclist2 = objvertices("ico.obj", 2)

def task_to_shoot_while_rotating(vec, axis, shottype, color, angle_interval, speed, lifespan):
	if abs(vec * axis) > 0.995 > 0: return lambda: 0

	binder = Entity(WORLD)
	binder.vec = vec

	def shot_dia(rot = Matrix3.RotationAxis(vec ^ (vec ^ axis), angle_interval)):
		shot = EntityShot(WORLD, shottype, color)
		shot.Velocity = binder.vec * speed
		shot.LifeSpan = lifespan

		shot.SetMotionInterpolationCurve(Vector2(0.3, 0.7), Vector2(0.3, 0.7), 43, False)

		def turn1():
			shot.Velocity = normalize(shot.Velocity) * 2 * Matrix3.RotationAxis(axis ^ normalize(shot.Velocity), RAD * 150)
			shot.SetMotionInterpolationCurve(Vector2(0.3, 0.7), Vector2(0.3, 0.7), 29, False)
		shot.AddTask(turn1, 0, 1, 45)

		def turn2():
			shot.Velocity = normalize(shot.Velocity) * 4 * Matrix3.RotationAxis(axis ^ normalize(shot.Velocity), RAD * 160)
		shot.AddTask(turn2, 0, 1, 75)

		shot.Spawn()

		binder.vec *= rot
	return shot_dia

axislist = [v * i for i in [-1, 1] for v in [Vector3.UnitX, Vector3.UnitY, Vector3.UnitZ]]

def task_list(tasks = [task_to_shoot_while_rotating(v, a, "DIA", 0xA0A000, RAD * 8, 6, 400) for v in veclist0 for a in axislist]):
	for task in tasks:
		task()

WORLD.AddTask(task_list, 4, 100, 0)

def shot_dia():
	for vec in veclist2:
		shot = EntityShot(WORLD, "DIA", 0xA00000)
		shot.Velocity = vec * 6
		shot.LifeSpan = 140
		shot.Spawn()
WORLD.AddTask(shot_dia, 30, 10, 30)
