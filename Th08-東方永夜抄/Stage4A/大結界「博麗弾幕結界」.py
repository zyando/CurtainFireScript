# -*- coding: utf-8 -*-

BORDER_DISTANCE_1 = 200
BORDER_DISTANCE_2 = 400

MGC_DISTANCE = 60

edge_list = [+Vector3(x, y, z) for x in [1, -1] for y in [1, -1] for z in [1, -1]]
face_list = [v * i for i in [1, -1] for v in Vector3.Units]

init_rot = Quaternion.RotationAxis(randomvec(), RAD * 30)

parent1 = EntityShot(WORLD, "BONE", 0)
parent1.Rot = init_rot
parent1.GetRecordedRot = lambda e: e.Rot
parent1()

parent2 = EntityShot(WORLD, "BONE", 0)
parent2.Rot = init_rot
parent2.GetRecordedRot = lambda e: e.Rot
parent2()

def rotate(binder = [Vector3.UnitY, Quaternion.RotationAxis(randomvec(), RAD * 0.2)]):
	rot = Quaternion.RotationAxis(binder[0], RAD * 0.4)
	parent1.Rot *= rot
	parent2.Rot *= ~rot
	binder[0] *= binder[1]
WORLD.AddTask(rotate, 1, 0, 150)

def get_collide_frame1(pos, velocity):
	return int(min([(BORDER_DISTANCE_1 + abs(pos[i])) / abs(velocity[i]) for i in range(3)]))
	
def get_collide_frame2(pos, velocity):
	return int(min([(BORDER_DISTANCE_2 - BORDER_DISTANCE_1) / abs(velocity[i]) for i in range(3)]))

red_scale_veclist = [Vector3.UnitZ * Matrix3.RotationX(RAD * 40) * Matrix3.RotationZ(RAD * 90 * i) for i in range(4)] + [Vector3.UnitZ]

for pos in edge_list:
	mgc = EntityShot(WORLD, "MAGIC_CIRCLE", 0xA00000, parent1)
	mgc.Pos = pos * MGC_DISTANCE * math.sqrt(3)
	mgc.LookAtVec = pos
	
	def shot_red_scale(mgc = mgc):
		for vec in red_scale_veclist:
			shot = EntityShot(WORLD, "SCALE", 0xA00000)
			shot.Pos = mgc.WorldPos
			shot.Velocity = vec * Matrix3.LookAt(mgc.WorldPos, Vector3.UnitY * parent1.Rot) * 6
			shot.LifeSpan = get_collide_frame1(shot.Pos, shot.Velocity)
			
			def on_collide(org = shot):
				shot = EntityShot(WORLD, "SCALE", 0xA00000)
				shot.Pos = org.Pos * -2
				shot.Velocity = org.Velocity
				shot.LifeSpan = get_collide_frame2(shot.Pos, shot.Velocity)
				shot()
			shot.AddTask(on_collide, 0, 1, shot.LifeSpan)
			shot()
	mgc.AddTask(shot_red_scale, 3, 300, 0)
	mgc()

white_scale_veclist = [Vector3.UnitZ * Matrix3.RotationX(RAD * 20) * Matrix3.RotationZ(RAD * 90 * (i + 0.5)) for i in range(4)]

for pos in face_list:
	mgc = EntityShot(WORLD, "MAGIC_CIRCLE", 0xA00000, parent2)
	mgc.Pos = pos * MGC_DISTANCE
	mgc.Upward = randomvec() ^ pos
	mgc.LookAtVec = pos
	
	def shot_red_scale(mgc = mgc):
		for vec in white_scale_veclist:
			shot = EntityShot(WORLD, "SCALE", 0xA0A0A0)
			shot.Pos = mgc.WorldPos
			shot.Velocity = vec * Matrix3.LookAt(mgc.WorldPos, Vector3.UnitY * parent2.Rot) * 6
			shot.LifeSpan = get_collide_frame1(shot.Pos, shot.Velocity)
			
			def on_collide(org = shot):
				shot = EntityShot(WORLD, "SCALE", 0xA0A0A0)
				shot.Pos = org.Pos * -2
				shot.Velocity = org.Velocity
				shot.LifeSpan = get_collide_frame2(shot.Pos, shot.Velocity)
				shot()
			shot.AddTask(on_collide, 0, 1, shot.LifeSpan)
			shot()
	mgc.AddTask(shot_red_scale, 3, 300, 0)
	mgc()

def shot_s():
	shot = EntityShot(WORLD, "S", 0xA0A0A0)
	shot.Velocity = randomvec() * 4
	shot.LifeSpan = get_collide_frame1(shot.Pos, shot.Velocity)
	
	def on_collide(org = shot):
		shot = EntityShot(WORLD, "S", 0xA0A0A0)
		shot.Pos = org.Pos * -2
		shot.Velocity = org.Velocity
		shot.LifeSpan = get_collide_frame2(shot.Pos, shot.Velocity)
		shot()
	shot.AddTask(on_collide, 0, 1, shot.LifeSpan)
	shot()
WORLD.AddTask(shot_s, 1, 0, 300)
