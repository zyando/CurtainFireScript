# -*- coding: utf-8 -*-

WORLD_REIMU_BOMB = CreateWorld(u"霊符「夢想妙珠」")

veclist = objvertices("ico.obj", 2)
octree = OctantNode(AABoundingBox(Vector3(1, 1, 1) * -4000, Vector3(1, 1, 1) * 4000), 128)
octree_keeping = OctantNode(AABoundingBox(Vector3(1, 1, 1) * -4000, Vector3(1, 1, 1) * 4000), 128)

class EntityMagicCircle(EntityShot):
	def __init__(self, world, shottype, color, scale):
		EntityShot.__init__(self, world, shottype, color, scale)
		self.hp = 25
		self.mgc_vec = Vector3()
		self.mgc_pos = Vector3()
		
	def SetDamage(self):
		if self.IsRemoved: return
		
		self.hp -= 1
		if self.hp <= 0:
			self.Remove()
			
			for i in range(64):
				particle = EntityShotStraight(WORLD, "DIA", 0x900070, Vector3(1, 1, 3))
				particle.Pos = self.Pos
				particle.Velocity = randomvec() * 12
				particle.LivingLimit = 10
				particle()
	
	def Hit(self, color):
		if self.IsRemoved: return
		
		self.AddBoneKeyFrame(self.RootBone, self.Pos, self.Rot, CubicBezierCurve.Line, 0)
		
		def shake():
			if self.IsRemoved: return
			self.AddBoneKeyFrame(self.RootBone, self.mgc_pos + randomvec() * random() * 40, self.Rot, CubicBezierCurve.Line, 0)
		self.AddTask(shake, 0, 20, 0)
		
		def shot_dia():
			if self.IsRemoved: return
			
			self.AddBoneKeyFrame(self.RootBone, self.mgc_pos, self.Rot, CubicBezierCurve.Line, 0)
			
			for i in range(40 + WORLD.FrameCount / 100):
				velocity = -self.mgc_vec * 0.5 + randomvec() * uniform(1, 2)
				livinglimit = min((400 if velocity * self.mgc_vec < 0 else 100, REIMU_BOMB_FRAME2 + randint(30, 40) - WORLD.FrameCount, get_time_to_vanish(self.Pos, velocity)))
				if livinglimit <= 0: continue
				
				shot = EntityShotStraight(WORLD, "DIA_BRIGHT", color)
				shot.Pos = self.Pos
				shot.Velocity = velocity
				shot.LivingLimit = livinglimit
				shot()
		self.AddTask(shot_dia, 0, 1, 20)

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

def shot_mgc(vec, shot_range):
	pos = HAND_BONE.WorldPos - Vector3.UnitZ * 1000 + vec * shot_range
	
	mgc = EntityMagicCircle(WORLD, "MAGIC_CIRCLE", 0x200001, 3)
	mgc.GetRecordedRot = lambda e: e.Rot
	mgc.Rot = Matrix3.LookAt(vec, randomvec())
	mgc.Pos = HAND_BONE.WorldPos
	mgc.Velocity = (pos - HAND_BONE.WorldPos) * (1.0 / 90)
	mgc.LivingLimit = REIMU_BOMB_FRAME2 + randint(30, 40) - WORLD.FrameCount
	mgc.mgc_pos = pos
	mgc.mgc_vec = vec
	
	def set_zero():
		mgc.Velocity *= 0
		octree.AddEntity(mgc)
		octree_keeping.AddEntity(mgc)
	mgc.AddTask(set_zero, 0, 1, 90)
	
	def on_remove(sender, e):
		octree.RemoveEntity(mgc)
	mgc.RemoveEvent += on_remove
	
	mgc()
pos_and_range_list = [(0.95, 800), (0.9, 760), (0.8, 720), (0.7, 680), (0.4, 640), (0.1, 620), (-0.1, 600)]

def get_mgc_vec(vec, shot_range, min_range = 600, max_range = 800):
	return +(vec + Vector3.UnitZ * (4 * (shot_range - min_range) / (max_range - min_range)))

mgc_poslist = [(v, r) for d, r in pos_and_range_list for v in [get_mgc_vec(v, r) for v in veclist] if v.z > d]

WORLD.AddTask(lambda: [shot_mgc(*mgc_poslist.pop()) for i in range(7) if len(mgc_poslist) > 0], 0, len(mgc_poslist) / 7 + 1, 140)

def shot_l(vec, color):
	shot = EntityShot(WORLD, "L", 0xFF00FF)
	shot.Velocity = vec * 4.0
	shot.Pos = HAND_BONE.WorldPos
	shot.LivingLimit = 320

	time_to_turn = int(600.0 / ((shot.Velocity * Matrix3(1, 1, 0)).Length() + 1e-6))
	
	def check_whether_collided():
		for entity, time in octree.TimeToCollide(shot.Pos, shot.Velocity, 100):
			if time <= time_to_turn:
				shot.AddTask(lambda e = entity: e.Hit(color), 0, 1, time)
	check_whether_collided()
	
	if time_to_turn < 5000:
		def turn():
			shot.Velocity *= Matrix3.RotationZ(RAD * 180)
			check_whether_collided()
		shot.AddTask(turn, 0, 1, time_to_turn)
	
	shot()

def bool_iter(bool_value = True):
	while True:
		yield bool_value
		bool_value = not bool_value

def get_vecs(v = +Vector3(1, 0, -1.2), gen = bool_iter()):
	return (+(TARGET_BONE.WorldPos - HAND_BONE.WorldPos), 0x400040), (v * Matrix3.RotationAxis(Vector3.UnitZ, RAD * random() * 360), 0x400000 if next(gen) else 0x000040)

WORLD.AddTask(lambda: [shot_l(*v) for v in get_vecs()], 120, 11, 400)

"""マインドアミュレット"""

WAY = 6
ANGLE_LIST = [RAD * 10, RAD * 20]

amulet_veclist = [Vector3(0, sin(a), cos(a)) * Matrix3.RotationAxis(Vector3.UnitZ, RAD * (360.0 / WAY) * i) for a in ANGLE_LIST for i in range(WAY)]
amulet_veclist.append(Vector3.UnitZ)

def shot_red_amullet(mat = [Matrix3.Identity, Matrix3.RotationAxis(Vector3.UnitZ, RAD * 4)]):
	if REIMU_SHOT_FLAG.Pos.y < 0.01: return

	mat[0] = mat[0] * mat[1]
	
	pos = Vector4(0, 0, 4, 1) * REIMU_HAND_BONE.WorldMat

	for vec in amulet_veclist:
		vec = vec * mat[0]
		shot = EntityShotStraight(WORLD, "AMULET", 0xA00000, 0.6)
		shot.Pos = pos
		shot.Velocity = vec * REIMU_HAND_BONE.WorldMat * 12.0
		
		shot.Upward = (vec ^ (vec ^ Vector3.UnitZ)) * REIMU_HAND_BONE.WorldMat
		shot.LivingLimit = 100
		
		entity, time = octree.MinTimeToCollide(shot.Pos, shot.Velocity, 40)
		
		if 3000 > time > 0:
			WORLD.AddTask(lambda count = REIMU_SHOT_FLAG.Pos.x: [entity.SetDamage() for i in range(count)], 0, 1, time)
			shot.LivingLimit = time
		shot()
WORLD.AddTask(shot_red_amullet, 3, 0, 0)

homing_veclist = [Vector3(sin(a) * i, 0, -cos(a)) for a in [RAD * 30, RAD * 45] for i in -1, 1]

def shot_homing_amulet(speed = 12):
	if REIMU_SHOT_FLAG.Pos.y < 0.01: return
	
	pos = Vector4(0, 0, 4, 1) * REIMU_HAND_BONE.WorldMat
	target = octree.Nearest(pos)
	
	for vec in homing_veclist:
		shot = EntityShot(WORLD, "AMULET", 0xA000A0, 0.6)
		shot.Pos = pos
		shot.Velocity = vec * REIMU_HAND_BONE.WorldMat * speed
		shot.Upward = (vec ^ (vec ^ Vector3.UnitZ)) * REIMU_HAND_BONE.WorldMat
		
		target_binder = [target]
		damage_func_binder = [target_binder[0].SetDamage]
		
		def hit(sender, args, shot = shot, damage_func_binder = damage_func_binder):
			damage_func_binder[0]()
		shot.RemoveEvent += hit
		
		def homing(shot = shot, target_binder = target_binder, damage_func_binder = damage_func_binder):
			if target_binder[0].IsRemoved:
				target_binder[0] = octree.Nearest(shot.Pos)
				damage_func_binder[0] = target_binder[0].SetDamage
			
			pos = target_binder[0].Pos
			
			vec = +shot.Velocity
			vec_to_target = +(pos - shot.Pos)
			alpha = (1 - vec * vec_to_target) * 0.4
			
			shot.Velocity = (vec + (vec_to_target - vec) * alpha) * speed
			shot.LivingLimit = shot.FrameCount + int((pos - shot.Pos).Length() / speed)
		shot.AddTask(homing, 0, 0, 0)
		shot()
WORLD.AddTask(shot_homing_amulet, 3, 0, 0)

"""霊符「夢想妙珠」"""

colors = 0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFFFF

def shot_reimu_bomb(speed = 16, veclist = objvertices("ico.obj", 0)):
	for vec in veclist:
		shot = EntityShot(WORLD_REIMU_BOMB, "M", colors[randint(0, len(colors) - 1)], 4)
		shot.Pos = Vector4(0, 0, 4, 1) * REIMU_HAND_BONE.WorldMat
		shot.Velocity = vec * REIMU_HAND_BONE.WorldMat * speed
		
		def homing(task, shot = shot):
			entity = octree_keeping.Nearest(shot.Pos)
			pos = entity.Pos
			
			vec = +shot.Velocity
			vec_to_target = +(pos - shot.Pos)
			alpha = (1 - vec * vec_to_target) * min(0.4, max(task.ExecutedCount - 20, 0) * 0.4 * 0.05)
			
			shot.Velocity = +(vec + (vec_to_target - vec) * alpha) * speed
			shot.LivingLimit = shot.FrameCount + int((pos - shot.Pos).Length() / speed)
		shot.AddTask(homing, 0, 0, 0, True)
		shot()
WORLD.AddTask(shot_reimu_bomb, 0, 1, REIMU_BOMB_FRAME1)
