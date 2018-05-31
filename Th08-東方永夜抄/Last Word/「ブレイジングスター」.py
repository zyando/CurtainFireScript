# -*- coding: utf-8 -*-

num_shot = 80
interval = 5

veclist = objvertices("ico.obj", 1)

bone = EntityMoving(WORLD)
bone.Velocity = Vector3.UnitZ * 12
bone()

def world_task(task):
	mat = Matrix3.RotationAxis(randomvec(), RAD * 180 * random())

	for vec in veclist:
		shot = EntityShot(WORLD, "STAR_M", 0xA00000 if task.ExecutedCount % 2 == 0 else 0x0000A0)
		shot.Pos = bone.WorldPos
		shot.Velocity = vec * 1.2 * mat
		shot.SetMotionInterpolationCurve(Vector2(0.1, 0.9), Vector2(0.1, 0.9), 60)

		def bezier(shot = shot):
			shot.SetMotionInterpolationCurve(Vector2(0.8, 0.2), Vector2(0.8, 0.2), 60)
		shot.AddTask(bezier, 0, 1, 60)

		def move(shot = shot):
			shot.Velocity *= 3.4
		shot.AddTask(move, 0, 1, 120)
		shot()
WORLD.AddTask(world_task, 3, 16, 0, True)
