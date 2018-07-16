# -*- coding: utf-8 -*-

veclist = []

for vec in [Vector3.UnitZ * Matrix3.RotationAxis(Vector3.UnitX, RAD * 25 * i) for i in range(-2, 3)]:
	way = 7
	for i in range(3):
		original = vec
		mat = Matrix3.RotationAxis(Vector3.UnitY, RAD * (80.0 / ((way - 1) / 2)))
		vec = vec * Matrix3.RotationAxis(Vector3.UnitY, RAD * -80.0)
		
		for j in range(way):
			veclist.append(vec * (1 + i) * 160)
			vec = vec * mat
		vec = original
		way += 2

for vec in veclist:
	parent = EntityShot(WORLD, "MAGIC_CIRCLE", 0x0000A0, 4)
	parent.GetRecordedRot = lambda e: e.Rot
	parent.Pos = CENTER_BONE.WorldPos + vec
	parent.Rot = Matrix3.LookAt(+vec, Vector3.UnitZ)
	
	def shot_laser(is_first = False, parent = parent, vec = +vec):
		if not is_first: vec = vec * Matrix3.RotationAxis(vec ^ randomvec(), RAD * random() * 60)
		
		laser = EntityShot(WORLD, "LASER_LINE", 0x0000A0, Vector3(5, 5, 4000))
		laser.GetRecordedRot = lambda e: e.Rot
		laser.Pos = parent.Pos
		laser.Rot = Matrix3.LookAt(vec, Vector3.UnitZ)
		
		morph = laser.CreateVertexMorph(0, lambda v: Vector3(-v.x * 0.9, -v.y * 0.9, 0))
		laser.AddMorphKeyFrame(morph, 1, 0)
		laser.AddMorphKeyFrame(morph, 1, 29)
		laser.AddMorphKeyFrame(morph, 0, 30)
		laser.AddMorphKeyFrame(morph, 0, 120)
		laser.AddMorphKeyFrame(morph, 1, 140)
		laser.LivingLimit = 140
		
		laser()
	parent.AddTask(shot_laser, 120, 6, 140)
	shot_laser(True)
	
	parent()

def shot_star():
	for i in range(16):
		shot = EntityShot(WORLD, "STAR_S", 0xA00000)
		shot.Pos = CENTER_BONE.WorldPos + Vector3(gauss(0, 1) * 600, gauss(0, 1) * 400, gauss(0, 1) * 40)
		shot.Velocity = Vector3.UnitZ * Matrix3.RotationAxis(Vector3.UnitZ ^ randomvec(), RAD * random() * 60) * uniform(4, 8)
		shot.LivingLimit = 450
		shot()
WORLD.AddTask(shot_star, 0, 400, 30)
