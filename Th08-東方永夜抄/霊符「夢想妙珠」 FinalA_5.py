# -*- coding: utf-8 -*-

WORLD_EFFECT = CreateWorld("ImpactEffect")

colors = 0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFFFF

pos_and_veclist = [
	(Vector3(-72, 203, 497), +Vector3(0, -0.1, -1)),
	(Vector3(74, 400, 601), +Vector3(0, -0.4, -1)),
	(Vector3(200, 280, 491), +Vector3(-0.2, -0.4, -1)),
	]

def shot_reimu_bomb(speed = 16):
	for pos, vec in pos_and_veclist:
		shot = EntityShot(WORLD, "M", colors[randint(0, len(colors) - 1)], 4)
		shot.Pos = pos
		shot.Velocity = vec * speed
		
		def homing(task, shot = shot):
			vec = +shot.Velocity
			vec_to_target = +(CENTER_BONE.WorldPos - shot.Pos)
			alpha = (1 - vec * vec_to_target) * 0.4

			shot.Velocity = +(vec + (vec_to_target - vec) * alpha) * speed
			shot.LivingLimit = shot.FrameCount + int((CENTER_BONE.WorldPos - shot.Pos).Length() / speed)
			
			if shot.LivingLimit <= shot.FrameCount + 1:
				WORLD.AddTask(impact_effect, 0, 40, 1)
		shot.AddTask(homing, 0, 0, 0, True)
		shot()
WORLD.AddTask(shot_reimu_bomb, 0, 1, REIMU_BOMB_FRAME2 - WORLD.FrameCount)

def impact_effect():
	for i in range(32):
		shot = EntityShot(WORLD_EFFECT, "DIA", 0xFFFFFF, Vector3(0.4, 0.4, 8))
		shot.Velocity = randomvec() * uniform(60, 100)
		shot.Pos = CENTER_BONE.WorldPos + shot.Velocity * random()
		shot.LivingLimit = randint(20, 30)
		shot()
