# -*- coding: utf-8 -*-

veclist1 = objvertices("ico.obj", 1)
veclist2 = objvertices("ico.obj", 3)

posList = [Vector3(40, 0, 0), Vector3(0, 40, 20)]

def world_task():
	posStack = posList[:]

	def shot_m_task():
		pos = randomvec() * 40
		mat = Matrix3.RotationAxis(randomvec(), RAD * 180 * random())
		
		def shot_m(task):
			for vec in veclist1:
				vec = vec * mat
				
				shot = EntityShot(WORLD, "M", 0x0000A0)
				shot.Pos = CENTER_BONE.WorldPos + vec * task.ExecutedCount * 20 + pos
				shot.LivingLimit = 90
				shot()
				
				def move(shot = shot, vec = vec):
					newShot = EntityShotStraight(WORLD, "M", 0xA00000)
					newShot.Pos = shot.Pos
					newShot.Velocity = vec * 4
					newShot.LivingLimit = 200
					newShot()
				shot.AddTask(move, 0, 1, shot.LivingLimit)
		WORLD.AddTask(shot_m, 2, 20, 30, True)
		
		def shot_bullet(prop, speed, limit, respaen_frame = 60):
			mat = Matrix3.RotationAxis(randomvec(), RAD * 180 * random())

			for vec in veclist2:
				vec = vec * mat

				shot = EntityShotStraight(WORLD, *prop)
				shot.Pos = CENTER_BONE.WorldPos
				shot.Velocity = vec * speed
				shot.LivingLimit = limit
				shot()

				def respawn(pos = shot.Pos, vec = vec):
					shot = EntityShotStraight(WORLD, *prop)
					shot.Pos = pos + vec * speed * respaen_frame
					shot.Velocity = vec * speed
					shot.LivingLimit = limit
					shot()
				WORLD.AddTask(respawn, 0, 1, respaen_frame)
		WORLD.AddTask(lambda: shot_bullet(("BULLET", 0xA00000), 4.8, 30), 0, 1, 30)
		WORLD.AddTask(lambda: shot_bullet(("BULLET", 0x0000A0), 4.5, 30), 0, 1, 30)
		WORLD.AddTask(lambda: shot_bullet(("BULLET", 0xA00000), 4.5, 28), 0, 1, 32)
		WORLD.AddTask(lambda: shot_bullet(("BULLET", 0x0000A0), 4.2, 28), 0, 1, 32)
		WORLD.AddTask(lambda: shot_bullet(("BULLET", 0xA00000), 4.2, 24), 0, 1, 36)
	WORLD.AddTask(shot_m_task, 90, 4, 0)
WORLD.AddTask(world_task, 0, 1, 0)
