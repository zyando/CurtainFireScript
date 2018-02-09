# -*- coding: utf-8 -*-

WORLD.MaxFrame = 3000

veclist = objvertices("ico.obj", 2)

def shot_dia(task, max_idx = 20.0):
	t = min(task.RunCount / max_idx, 1)

	for vec in veclist:
		if vec.z < -0.95: continue

		shot = EntityShot(WORLD, "DIA", 0x000040)
		shot.Velocity = (Vector3.UnitZ + (vec - Vector3.UnitZ) * t) * 12.0
		shot.LivingLimit = 100
		shot.ModelData.Materials[0].Shininess = 130
		shot()
WORLD.AddTask(shot_dia, 5, 48, 0,True)

mgcrl_list = []

def shot_mgcrl(vec, shot_range):
	pos = OWNER_BONE.WorldPos - Vector3.UnitZ * 800 + vec * shot_range

	mgcrl = EntityShot(WORLD, "MAGIC_CIRCLE", 0x300010, 2)
	mgcrl.GetRecordedRot = lambda e, rot = Matrix3.LookAt(vec, randomvec()): rot
	mgcrl.Velocity = (pos - OWNER_BONE.WorldPos) * (1.0 / 90)

	def set_zero(): mgcrl.Velocity *= 0
	mgcrl.AddTask(set_zero, 0, 1, 90)

	def shake_and_shot_dia(color = 0x000040 if abs(pos.x) < 50 else (0x400000 if pos.x > 50 else 0x400040)):
		mgcrl.AddRootBoneKeyFrame()
		def shake(): mgcrl.Pos = pos + randomvec() * random() * 40
		mgcrl.AddTask(shake, 0, 20, 0)

		def shot_dia():
			mgcrl.Pos = pos
			for i in range(40 + WORLD.FrameCount / 100):
				shot = EntityShot(WORLD, "DIA", color)
				shot.Pos = mgcrl.Pos
				shot.Velocity = -vec + (randomvec() * (1 + random() * 1.2) * 2 + vec) * 0.6
				shot.LivingLimit = 400 if shot.Velocity * vec < 0 else 100
				shot.ModelData.Materials[0].Shininess = 130
				shot()
		mgcrl.AddTask(shot_dia, 0, 1, 20)
	mgcrl_list.append((pos, shake_and_shot_dia))
	mgcrl()
pos_and_range_list = [(0.95, 600), (0.9, 560), (0.8, 520), (0.7, 480), (0.4, 440), (0.1, 420), (-0.1, 400)]

def get_mgcrl_vec(vec, shot_range, min_range = 400, max_range = 600):
	return +(vec + Vector3.UnitZ * (4 * (shot_range - min_range) / (max_range - min_range)))

mgcrl_poslist = []
for d, r in pos_and_range_list:
	mgcrl_poslist.extend([(v, r) for v in [get_mgcrl_vec(v, r) for v in veclist] if v.z > d])

WORLD.AddTask(lambda: [shot_mgcrl(*mgcrl_poslist.pop()) for i in range(7) if len(mgcrl_poslist) > 0], 0, len(mgcrl_poslist) / 7 + 1, 220)

def shot_l(vec):
	shot = EntityShot(WORLD, "L", 0xFF00FF)
	shot.Velocity = vec * 4.0
	shot.Pos = OWNER_BONE.WorldPos
	shot.LivingLimit = 320

	def check_weather_collided(collided_list = [], xy_plane_scale = Matrix3(1, 1, 0)):
		[(collided_list.append(pos), f()) for pos, f in mgcrl_list if (pos not in collided_list and (pos - shot.Pos).Length() < 80)]

		if (shot.Pos * xy_plane_scale).Length() > 400: shot.Velocity *= Matrix3.RotationAxis(Vector3.UnitZ, RAD * 180)
	shot.AddTask(check_weather_collided, 0, 0, 0)
	shot()

def get_vecs(v = +Vector3(1, 0, -1.2)):
	return +(TARGET_BONE.WorldPos - OWNER_BONE.WorldPos), v * Matrix3.RotationAxis(Vector3.UnitZ, RAD * random() * 360)

WORLD.AddTask(lambda: [shot_l(v) for v in get_vecs()], 120, 20, 480)
