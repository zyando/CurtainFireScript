# -*- coding: utf-8 -*-

SCALE = 4

parent = EntityShot(WORLD, "BONE", 0)
def record(): parent.Pos = HAND_BONE.WorldPos
WORLD.AddTask(record, 0, 0, 0)
parent()

obj = WavefrontObject("space_filling.obj", lambda v: v * 25 * SCALE)
connected_vtx_dict = {v : obj.create_list_connected_vertex(v) for v in obj.veclist}

def task():
	pos_and_target_list = []
	mat = Matrix3.RotationAxis(Vector3.UnitZ, RAD * random() * 360) * HAND_BONE.WorldRot

	def shot_laser(vtx, level, offset):
		for connected_vtx in connected_vtx_dict[vtx]:
			if (vtx, connected_vtx) in pos_and_target_list or (connected_vtx, vtx) in pos_and_target_list: continue

			pos_and_target_list.append((vtx, connected_vtx))

			vec = connected_vtx - vtx
			length = vec.Length()

			shot = EntityShot(WORLD, "M", 0xA00000)
			shot.Pos = offset + vtx * mat
			shot.LivingLimit = 5
			shot.Velocity = vec * mat * (1.0 / shot.LivingLimit)
			shot()

			laser = EntityShot(WORLD, "LASER_LINE", 0xA00000, Vector3(1 * SCALE, 1 * SCALE, length))
			laser.GetRecordedRot = lambda e: e.Rot
			laser.Pos = offset + vtx * mat
			laser.Rot = Matrix3.LookAt(+(vec * mat), Vector3.UnitY)
			laser.LivingLimit = 100

			morph = laser.CreateVertexMorph(lambda v: Vector3(v.x * -0.95, v.y * -0.95, 0))
			laser.AddMorphKeyFrame(morph, 1, 0)
			laser.AddMorphKeyFrame(morph, 0, 5)
			laser.AddMorphKeyFrame(morph, 0, 95)
			laser.AddMorphKeyFrame(morph, 1, 100)

			laser.AddTask(lambda v = connected_vtx: shot_laser(v, level + 1, offset), 0, 1, 5)
			laser()
	shot_laser(Vector3.Zero, 0, HAND_BONE.WorldPos)
WORLD.AddTask(task, 200, 4, 2)

veclist3 = objvertices("ico.obj", 3)

def shot_dia():
	mat = HAND_BONE.WorldRot * Matrix3.RotationAxis(randomvec(), RAD * random() * 10)

	for vec in veclist3:
		if vec * Vector3.UnitZ > -0.7: continue

		shot = EntityShot(WORLD, "DIA", 0x0000A0)
		shot.Pos = HAND_BONE.WorldPos
		shot.Velocity = vec * mat * 4
		shot.LivingLimit = 400

		shot()
WORLD.AddTask(shot_dia, 8, 100, 2)

veclist2 = objvertices("ico.obj", 2)

def shot_l():
	for vec in veclist2:
		if vec * Vector3.UnitZ < -0.3: continue

		shot = EntityShot(WORLD, "L", 0xFF0000)
		shot.Pos = HAND_BONE.WorldPos
		shot.Velocity = vec * HAND_BONE.WorldRot * 1.2
		shot.LivingLimit = 800

		shot()
WORLD.AddTask(shot_l, 30, 28, 2)
