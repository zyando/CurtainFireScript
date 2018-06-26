# -*- coding: utf-8 -*-

veclist = objvertices("ico.obj", 0)

colors = 0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFFFF

def shot_homing_amulet(speed = 5):
	for vec in veclist:
		shot = EntityShot(WORLD, "M", colors[randint(0, len(colors) - 1)], 4)
		shot.Pos = Vector4(0, 0, 4, 1) * REIMU_HAND_BONE.WorldMat
		shot.Velocity = vec * REIMU_HAND_BONE.WorldMat * speed
		shot.Upward = (vec ^ (vec ^ Vector3.UnitZ)) * REIMU_HAND_BONE.WorldMat

		def homing(shot = shot):
			target_pos = get_targetpos(shot.Pos)
			
			length = shot.Velocity.Length()
			vec = shot.Velocity * (1.0 / length)
			vec_to_target = +(target_pos - shot.Pos)
			alpha = (1 - min(1, vec * vec_to_target * 1.5)) * 0.6

			shot.Velocity = (vec + (vec_to_target - vec) * alpha) * length * 1.05

			if (target_pos - shot.Pos).Length() <= 60:
				shot.LivingLimit = 1
				impact_effect(shot.Pos)
		shot.AddTask(homing, 0, 0, 0)
		shot()
WORLD.AddTask(shot_homing_amulet, 0, 1, REIMU_BOMB_FRAME)

def impact_effect(pos):
	for i in range(512):
		shot = EntityShot(WORLD, "DIA", 0xFFFFFF, Vector3(1, 1, 12))
		shot.Pos = pos
		shot.Velocity = randomvec() * uniform(60, 100)
		shot.LivingLimit = 45
		shot()
