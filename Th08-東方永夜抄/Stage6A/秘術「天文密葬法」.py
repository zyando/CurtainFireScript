# -*- coding: utf-8 -*-

WORLD.MaxFrame = 3000

veclist = objvertices("ico.obj", 2)

def shot_dia(task, max_idx = 20.0):
	t = min(task.ExecutedCount / max_idx, 1)

	for vec in veclist:
		if vec.z < -0.95: continue

		shot = EntityShotStraight(WORLD, "DIA_BRIGHT", 0x000040)
		shot.Pos = HAND_BONE.WorldPos
		shot.Velocity = (Vector3.UnitZ + (vec - Vector3.UnitZ) * t) * 12.0
		shot.LivingLimit = 100
		shot()
WORLD.AddTask(shot_dia, 5, 32, 0, True)

mgc_list = []

def shot_mgc(vec, shot_range):
	pos = HAND_BONE.WorldPos - Vector3.UnitZ * 1000 + vec * shot_range
	
	mgc = EntityShot(WORLD, "MAGIC_CIRCLE", 0x300010, 3)
	mgc.GetRecordedRot = lambda e: mgc.Rot
	mgc.Rot = Matrix3.LookAt(vec, randomvec())
	mgc.Pos = HAND_BONE.WorldPos
	mgc.Velocity = (pos - HAND_BONE.WorldPos) * (1.0 / 90)
	
	def damage(hp_binder = [80]):
		hp_binder[0] -= 1
		if hp_binder[0] <= 0:
			mgc.Remove()

	def on_remove(sender, args):
		if args.IsFinalize: return
		
		global mgc_list
		mgc_list = [t for t in mgc_list if t[0] != mgc]
		
		for i in range(64):
			particle = EntityShotStraight(WORLD, "DIA", 0x900070, Vector3(1, 1, 3))
			particle.Pos = mgc.Pos
			particle.Velocity = randomvec() * 12
			particle.LivingLimit = 10
			particle()
	mgc.RemoveEvent += on_remove

	def set_zero(): mgc.Velocity *= 0
	mgc.AddTask(set_zero, 0, 1, 90)

	def shake_and_shot_dia(color = (0x000040 if abs(pos.x) < 50 else (0x400000 if pos.x > 50 else 0x400040))):
		for i in range(21):
			mgc.AddBoneKeyFrame(mgc.RootBone, pos + ((randomvec() * random() * 40) if 0 < i < 20 else Vector3.Zero), mgc.Rot, CubicBezierCurve.Line, i)

		def shot_dia():
			for i in range(40 + WORLD.FrameCount / 100):
				shot = EntityShotStraight(WORLD, "DIA_BRIGHT", color)
				shot.Pos = mgc.Pos
				shot.Velocity = -vec + (randomvec() * (1 + random() * 1.2) * 2 + vec) * 0.6
				shot.LivingLimit = 400 if shot.Velocity * vec < 0 else 100
				shot()
		mgc.AddTask(shot_dia, 0, 1, 20)
	mgc_list.append((mgc, shake_and_shot_dia, damage))
	mgc()
pos_and_range_list = [(0.95, 800), (0.9, 760), (0.8, 720), (0.7, 680), (0.4, 640), (0.1, 620), (-0.1, 600)]

def get_mgc_vec(vec, shot_range, min_range = 600, max_range = 800):
	return +(vec + Vector3.UnitZ * (4 * (shot_range - min_range) / (max_range - min_range)))

mgc_poslist = []
for d, r in pos_and_range_list:
	mgc_poslist.extend([(v, r) for v in [get_mgc_vec(v, r) for v in veclist] if v.z > d])

WORLD.AddTask(lambda: [shot_mgc(*mgc_poslist.pop()) for i in range(7) if len(mgc_poslist) > 0], 0, len(mgc_poslist) / 7 + 1, 140)

def calc_collided_mgc_list(pos, velocity, r):
	vec = +velocity
	speed = velocity.Length()

	def calc(target_pos):
		vec_to_target = target_pos - pos
		a = vec_to_target * vec

		f2 = r * r - vec_to_target * vec_to_target + a * a

		if f2 < 0:
			return 0xFFFFFF

		t = a - math.sqrt(f2)
		return t / speed
	return [(calc(mgc.Pos), mgc, shake_func, damage_func) for mgc, shake_func, damage_func in mgc_list]

def calc_time_to_collide(pos, velocity, r):
	time_list = calc_collided_mgc_list(pos, velocity, r)
	min_time = min(time_list, key = lambda t: t[0])
	return min_time[0] != 0xFFFFFF, min_time[0], min_time[1], min_time[2], min_time[3]

def shot_l(vec):
	shot = EntityShot(WORLD, "L", 0xFF00FF)
	shot.Velocity = vec * 4.0
	shot.Pos = HAND_BONE.WorldPos
	shot.LivingLimit = 320

	time_to_turn = int(600.0 / ((shot.Velocity * Matrix3(1, 1, 0)).Length() + 1e-6))
	
	def check_whether_collided():
		for time, mgc, shake_func, damage_func in calc_collided_mgc_list(shot.Pos, shot.Velocity, 100):
			if time <= time_to_turn:
				shot.AddTask(shake_func, 0, 1, time)
	check_whether_collided()
	
	if time_to_turn < WORLD.MaxFrame:
		def turn():
			shot.Velocity *= Matrix3.RotationZ(RAD * 180)
			check_whether_collided()
		shot.AddTask(turn, 0, 1, time_to_turn)
	
	shot()

def get_vecs(v = +Vector3(1, 0, -1.2)):
	return +(TARGET_BONE.WorldPos - HAND_BONE.WorldPos), v * Matrix3.RotationAxis(Vector3.UnitZ, RAD * random() * 360)

WORLD.AddTask(lambda: [shot_l(v) for v in get_vecs()], 120, 20, 400)

"""マインドアミュレット"""

WAY = 6
ANGLE_LIST = [RAD * 10, RAD * 20]

amulet_veclist = [Vector3(0, sin(a), cos(a)) * Matrix3.RotationAxis(Vector3.UnitZ, RAD * (360.0 / WAY) * i) for a in ANGLE_LIST for i in range(WAY)]
amulet_veclist.append(Vector3.UnitZ)

def shot_red_amullet(mat = [Matrix3.Identity, Matrix3.RotationAxis(Vector3.UnitZ, RAD * 4)]):
	if SHOT_FLAG.Pos.Length() < 0.01: return

	mat[0] = mat[0] * mat[1]

	for vec in amulet_veclist:
		vec = vec * mat[0]
		shot = EntityShotStraight(WORLD, "AMULET", 0xA00000, 0.8)
		shot.Pos = Vector4(0, 0, 4, 1) * REIMU_HAND_BONE.WorldMat
		shot.Velocity = vec * REIMU_HAND_BONE.WorldMat * 12.0
		shot.Upward = (vec ^ (vec ^ Vector3.UnitZ)) * REIMU_HAND_BONE.WorldMat

		is_successed, time, mgc, shake_func, damage_func = calc_time_to_collide(shot.Pos, shot.Velocity, 40)

		if is_successed:
			mgc.AddTask(damage_func, 0, 1, time)

			shot.LivingLimit = time
		shot()
WORLD.AddTask(shot_red_amullet, 3, 0, 0)

homing_veclist = [Vector3(sin(a) * i, 0, -cos(a)) for a in [RAD * 30, RAD * 45] for i in -1, 1]

def calc_nearest_mgc(pos):
	distance_list = [((pos - mgc.Pos).Length(), mgc, damage_func) for mgc, shake_func, damage_func in mgc_list]
	min_distance = min(distance_list, key = lambda t: t[0])
	return min_distance[1], min_distance[2]

def shot_homing_amulet(speed = 12):
	if SHOT_FLAG.Pos.Length() < 0.01: return

	for vec in homing_veclist:
		shot = EntityShot(WORLD, "AMULET", 0xA000A0, 0.8)
		shot.Pos = Vector4(0, 0, 4, 1) * REIMU_HAND_BONE.WorldMat
		shot.Velocity = vec * REIMU_HAND_BONE.WorldMat * speed
		shot.Upward = (vec ^ (vec ^ Vector3.UnitZ)) * REIMU_HAND_BONE.WorldMat

		damage_func_binder = [None]

		def hit(sender, args, shot = shot):
			if damage_func_binder[0] != None:
				damage_func_binder[0]()
		shot.RemoveEvent += hit

		def homing(shot = shot):
			mgc, damage_func = calc_nearest_mgc(shot.Pos)
			damage_func_binder[0] = damage_func

			vec = +shot.Velocity
			vec_to_target = +(mgc.Pos - shot.Pos)
			alpha = (1 - vec * vec_to_target) * 0.4

			shot.Velocity = (vec + (vec_to_target - vec) * alpha) * speed
			shot.LivingLimit = shot.FrameCount + int((mgc.Pos - shot.Pos).Length() / speed)
		shot.AddTask(homing, 0, 0, 0)
		shot()
WORLD.AddTask(shot_homing_amulet, 3, 0, 0)
