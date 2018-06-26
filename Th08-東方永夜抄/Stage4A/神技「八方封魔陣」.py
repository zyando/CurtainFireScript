# -*- coding: utf-8 -*-

veclist_ico0 = objvertices("ico.obj", 0)
veclist_ico2 = objvertices("ico.obj", 2)
veclist_ico_y = objvertices("ico.obj", 0)

def shot_omnidirectinal():
	for vec in veclist_ico0:
		shot = EntityShot(WORLD, "AMULET", 0xA00000)
		shot.Velocity = vec * 6
		shot.Pos = +shot.Velocity * 20
		shot.LivingLimit = 270

		mat = Matrix3(1, 0, 0, 0, 0, 1, 0, 1, 0) * Matrix3.LookAt(+vec, Vector3.UnitY)

		def divide(src = shot, src_vec = vec, mat = mat):
			for vec in veclist_ico_y:
				vec = vec * mat
				dot = vec * src_vec

				if -0.99 < dot < 0.99:
					shot = EntityShotStraight(WORLD, "AMULET", 0xA00000 if 0 < dot else 0xFFD700)
					shot.Pos = src.Pos
					shot.Velocity = +vec * 6
					shot.Upward = src_vec
					shot.LivingLimit = 240
					shot()
		shot.AddTask(divide, 0, 1, 50)
		shot()
WORLD.AddTask(shot_omnidirectinal, 4, 100, 0)

def shot_every_directinal():
	def shot_s(task):
		mat = Matrix3.RotationAxis(randomvec(), RAD * random() * 20)

		for vec in veclist_ico2:
			vec  = vec * mat
			shot = EntityShot(WORLD, "S", 0xFFFFFF)
			shot.Velocity = vec * (12 - task.ExecutedCount * 0.6)
			shot.Pos = +shot.Velocity * 10
			shot.SetMotionInterpolationCurve(Vector2(0.2, 0.8), Vector2(0.2, 0.8), 30)
			shot.LivingLimit = 40

			def stop(shot = shot, vec = vec): shot.Velocity *= 0
			shot.AddTask(stop, 0, 1, 30)

			def shot_red_scale(src = shot, vec = vec):
				shot = EntityShot(WORLD, "SCALE", 0xA00000)
				shot.Pos = src.Pos
				shot.LookAtVec = vec
				shot.LivingLimit = 100

				def move(shot = shot): shot.Velocity = vec * 6
				shot.AddTask(move, 0, 1, 20)

				shot()
			shot.AddTask(shot_red_scale, 0, 1, 40)
			shot()
	WORLD.AddTask(shot_s, 3, 5, 0, True)
WORLD.AddTask(shot_every_directinal, 60, 4, 60)
