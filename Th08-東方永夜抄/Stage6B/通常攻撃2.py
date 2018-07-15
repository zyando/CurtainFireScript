# -*- coding: utf-8 -*-
veclist = []

for vec in [Vector3.UnitZ * Matrix3.RotationAxis(Vector3.UnitX, RAD * 25 * i) for i in range(-2, 3)]:
	way = 7
	for i in range(3):
		original = vec
		mat = Matrix3.RotationAxis(Vector3.UnitY, RAD * (80.0 / ((way - 1) / 2)))
		vec = vec * Matrix3.RotationAxis(Vector3.UnitY, RAD * -80.0)
		
		for j in range(way):
			veclist.append(vec * (1 + i) * 80)
			vec = vec * mat
		vec = original
		way += 2

for vec in veclist:
	parent = EntityShot(WORLD, "MAGIC_CIRCLE", 0x0000A0, 2)
	parent.GetRecordedRot = lambda e: e.Rot
	parent.Pos = CENTER_BONE.WorldPos + vec
	parent.Rot = Matrix3.LookAt(+vec, Vector3.UnitZ)
	
	def shot_s(parent = parent, vec = +vec, binder = [Vector3.UnitZ, Matrix3.RotationY(RAD * 10)]):
		shot = EntityShot(WORLD, "S", 0x0000A0)
		shot.Pos = parent.Pos
		shot.Velocity = binder[0] * Matrix3.RotationAxis(randomvec(), RAD * 90 * gauss()) * 4
		shot.LivingLimit = 300
		shot()
		
		binder[0] *= binder[1]
		
	parent.AddTask(shot_s, 4, 120, randint(0, 4))
	
	parent()
