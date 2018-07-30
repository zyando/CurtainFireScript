# -*- coding: utf-8 -*-
veclist = []

for r in range(3):
	way_v = 5 + r * 2
	way_h = 7 + r * 2
	
	vec = Vector3.UnitZ * Matrix3.RotationX(RAD * -50)
	for vec in [vec * Matrix3.RotationX(RAD * (100.0 / (way_v - 1)) * i) for i in range(way_v)]:
		mat = Matrix3.RotationAxis(Vector3.UnitY, RAD * (160.0 / (way_h - 1)))
		vec = vec * Matrix3.RotationAxis(Vector3.UnitY, RAD * -80.0)
		
		for j in range(way_h):
			veclist.append(vec * (1 + r) * 160)
			vec = vec * mat

for vec in veclist:
	parent = EntityShot(WORLD, "MAGIC_CIRCLE", 0x0000A0, 4)
	parent.Pos = CENTER_BONE.WorldPos
	parent.Velocity = vec * (1.0 / 30) * HAND_BONE.WorldRot
	parent.SetMotionInterpolationCurve(Vector2(0.2, 0.8), Vector2(0.2, 0.8), 30)
	
	def pause(p = parent): p.Velocity *= 0
	parent.AddTask(pause, 0, 1, 30)
	
	def shot_s(parent = parent, vec = +vec, binder = [Vector3.UnitZ, Matrix3.RotationY(RAD * 10)]):
		shot = EntityShot(WORLD, "S", 0x0000A0)
		shot.Pos = parent.Pos + randomvec() * gauss(0, 80)
		
		for i in range(3):
			shot.Pos[i] -= shot.Pos[i] % 3
		
		shot.LivingLimit = 300
		shot()
		
		def move(v = binder[0] * Matrix3.RotationAxis(randomvec(), RAD * 90 * gauss()) * 5):
			shot.Velocity = v
		shot.AddTask(move, 0, 1, 60)
		
		binder[0] *= binder[1]
	parent.AddTask(shot_s, 10, 120, 75 + randint(0, 10))
	parent()
