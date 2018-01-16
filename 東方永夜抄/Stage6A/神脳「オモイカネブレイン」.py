# -*- coding: utf-8 -*-

way_of_laser = 30
laser_veclist = []

for angle in RAD * 20, RAD * 40:
	vec = Vector3(0, 0, 1) * Matrix3.RotationAxis(Vector3.UnitX, angle)
	laser_veclist.extend([vec * Matrix3.RotationAxis(Vector3.UnitZ, RAD * (360.0 / way_of_laser) * i) for i in range(way_of_laser)])

veclist = []
objvertices("ico.obj", lambda v: veclist.append(+v), 2)

def laser_and_dia_task(axis, interval_of_shoot = 4, time_to_stop = 480.0, wati_time = 50):
	parent = EntityShot(WORLD, "BONE", 0xFFFFFF)
	parent.Recording = Recording.LocalMat
	parent.Pos = Vector3(0, 0, -300)
	parent.LivingLimit = time_to_stop + wati_time + 30
	
	def rotate_and_shot(rot = Quaternion.RotationAxis(axis, RAD * 300.0 * (interval_of_shoot / time_to_stop))): parent.Rot *= rot
	parent.AddTask(rotate_and_shot, interval_of_shoot, time_to_stop / interval_of_shoot, wati_time)
	
	def shot_dia():
		ignore_vec = -Vector3.UnitZ * parent.Rot
		
		for vec in veclist:
			if vec * ignore_vec > 0.75: continue
			
			shot = EntityShot(WORLD, "DIA", 0xA00000)
			shot.Pos = parent.WorldPos
			shot.Velocity = vec * 12.0
			shot.LivingLimit = 100
			shot()
	parent.AddTask(shot_dia, interval_of_shoot, 0, 0)

	def shot_laser():
		for vec in laser_veclist:
			laser = EntityShot(WORLD, "LASER", 0x0000A0, parent)
			laser.Recording = Recording.LocalMat
			laser.Rot = Matrix3.LookAt(vec, Vector3.UnitY)
			laser.LivingLimit = time_to_stop + wati_time + 30
			
			if laser.ModelData.OwnerEntities.Count == 1:
				scale = Matrix3(20, 0, 0, 0, 20, 0, 0, 0, 4000)
				for vert in laser.ModelData.Vertices: vert.Pos *= scale
			
			morph = laser.CreateVertexMorph(lambda v: Vector3(v.x * -0.95, v.y * -0.95, 0))
			laser.AddMorphKeyFrame(morph, 1, 0)
			laser.AddMorphKeyFrame(morph, 1, 20)
			laser.AddMorphKeyFrame(morph, 0, 30)
			laser.AddMorphKeyFrame(morph, 0, laser.LivingLimit - 30)
			laser.AddMorphKeyFrame(morph, 1, laser.LivingLimit)
			
			laser()
	parent.AddTask(shot_laser, time_to_stop + 30, 1, 20)
	
	parent()
WORLD.AddTask(lambda: laser_and_dia_task(randomvec() ^ Vector3.UnitZ), 0, 1, 0)

def shoot_dia_while_rotating(vec, axis):
	axis = vec ^ (vec ^ axis)
	
	def shot_dia(task, vec_ = [vec], rot = Quaternion.RotationAxis(axis, RAD * 4)):
		if task.RunCount % 6 < 4:
			for i in range(2):
				shot = EntityShot(WORLD, "DIA", 0x0000A0)
				shot.Pos = Vector3(0, 0, 0)
				shot.Velocity = vec_[0] * (i + 1) * 2.0
				shot.LivingLimit = 200 * (i + 1)
				shot()
		vec_[0] *= rot * rot
	WORLD.AddTask(shot_dia, 1, 600, 0, True)
axislist = []
objvertices("ico.obj", lambda v: axislist.append(+v), 0)

for axis in axislist:
	for vec in [Vector3.UnitZ]:
		shoot_dia_while_rotating(axis, vec)
