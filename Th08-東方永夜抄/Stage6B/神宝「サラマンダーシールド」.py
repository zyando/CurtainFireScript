# -*- coding: utf-8 -*-

way = 16
angle = RAD * 50

matrices = Matrix3(1, 0, 0, 0, 1, 0, 0, 0, 1), Matrix3(0, 1, 0, 0, 0, 1, 1, 0, 0), Matrix3(0, 0, 1, 1, 0, 0, 0, 1, 0)

vec_axis_list = []
for i in range(way):
	vec = -Vector3.UnitZ * Matrix3.RotationX(angle) * Matrix3.RotationY(RAD * (360.0 / way) * i)
	axis = vec ^ (vec ^ Vector3.UnitY)
	vec *= Matrix3.RotationAxis(axis, RAD * (360.0 / way) * -i)
	
	for mat in matrices[0:1]:
		vec_axis_list.append((vec * mat, axis * mat))

def task(vec, axis, veclist = objvertices("ico_y.obj", 0)):
	def shot_s(binder = [vec], rot = Quaternion.RotationAxis(axis, RAD * 10)):
		trans_mat = Matrix3(1, 0, 0, 0, 0, 1, 0, 1, 0) * Matrix3.LookAt(-binder[0], Vector3.UnitY)
		
		for v in veclist:
			v *= trans_mat
			
			if v * binder[0] <= 0: continue
			
			shot = EntityShotStraight(WORLD, "S", 0xFF0000)
			shot.Pos = binder[0] * 160
			shot.Velocity = v * 4
			shot.LifeSpan = 200
			shot.Spawn()
		
		binder[0] *= rot
	WORLD.AddTask(shot_s, 2, 200, 0)

for vec, axis in vec_axis_list:
	task(vec, axis)
	task(vec, -axis)

def laser_task(pos):
	parent = EntityShot(WORLD, "M", 0xFF0000)
	parent.Pos = pos
	
	def short_laser():
		shot = EntityShotStraight(WORLD, "DIA", 0xFF0000, Vector3(2, 2, 16))
		shot.Pos = parent.Pos
		shot.Velocity = +(TARGET_BONE.WorldPos - shot.Pos) * 12
		shot.LifeSpan = 120
		shot.Spawn()
	parent.AddTask(short_laser, 20, 10, 60)
	
	def long_laser():
		shot = EntityShot(WORLD, "LASER_LINE", 0xFF0000, Vector3(5, 5, 4000))
		shot.Pos = parent.Pos
		shot.LookAtVec = +(TARGET_BONE.WorldPos - shot.Pos) * 12
		shot.LifeSpan = 35
		
		morph = shot.CreateVertexMorph(0, lambda v: Vector3(v.x * -0.99, v.y * -0.99, 0))
		shot.AddMorphKeyFrame(morph, 1, 0)
		shot.AddMorphKeyFrame(morph, 0, 15)
		
		shot.Spawn()
	parent.AddTask(long_laser, 60, 5, 90)
	parent()

for pos in [Vector3(x * 100, y * 100, 0) for x in [1, -1] for y in [1, -1]]:
	laser_task(pos)
