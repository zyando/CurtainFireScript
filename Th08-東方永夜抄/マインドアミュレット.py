# -*- coding: utf-8 -*-

def shot_red_amullet():
	if abs(REIMU_SHOT_FLAG.Pos.y) < 0.01: return
	hand_mat = OPTION_CENTER_BONE.LocalMat
	
	for bone in OPTION_BALL_BONES:
		mat = bone.WorldMat
		
		for i in range(randint(1, 3)):
			shot = EntityShot(WORLD, "AMULET", 0xA00000, 0.4)
			shot.Pos = mat.Translation
			shot.Velocity = Vector3.UnitZ * hand_mat * Matrix3.RotationAxis(randomvec(), RAD * 10) * 12 * REIMU_SHOT_FLAG.Pos.y
			shot.Upward = randomvec()
			shot()
WORLD.AddTask(shot_red_amullet, 0, 0, 0)

homing_veclist = [Vector3(sin(a) * i, 0, -cos(a)) for a in [RAD * 30, RAD * 45] for i in -1, 1]

def shot_homing_amulet(speed = 12):
	if REIMU_SHOT_FLAG.Pos.x < 0.01: return
	
	for vec in homing_veclist:
		shot = EntityShot(WORLD, "AMULET", 0xA000A0, 0.4)
		shot.Pos = Vector4(0, 0, 4, 1) * REIMU_HAND_BONE.WorldMat
		shot.Velocity = vec * REIMU_HAND_BONE.WorldMat * speed
		shot.Upward = (vec ^ (vec ^ Vector3.UnitZ)) * REIMU_HAND_BONE.WorldMat
		
		def homing(shot = shot):
			vec = +shot.Velocity
			vec_to_target = +(CENTER_BONE.WorldPos - shot.Pos)
			alpha = (1 - vec * vec_to_target) * 0.4
			
			shot.Velocity = (vec + (vec_to_target - vec) * alpha) * speed
			shot.LivingLimit = shot.FrameCount + int((CENTER_BONE.WorldPos - shot.Pos).Length() / speed)
		shot.AddTask(homing, 0, 0, 0)
		shot()
WORLD.AddTask(shot_homing_amulet, 3, 0, 0)
