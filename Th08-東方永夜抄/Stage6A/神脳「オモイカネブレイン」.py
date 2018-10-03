# -*- coding: utf-8 -*-

WORLD_SUB = CreateWorld(PRESET_FILENAME + "_Sub")

way_of_laser = 60
laser_veclist = []

for angle in RAD * 20, RAD * 40:
	vec = Vector3(0, 0, -1) * Matrix3.RotationAxis(Vector3.UnitX, angle)
	laser_veclist.extend([vec * Matrix3.RotationAxis(Vector3.UnitZ, RAD * (360.0 / way_of_laser) * i) for i in range(way_of_laser)])

veclist = objvertices("ico.obj", 2)

def laser_and_dia_task(task, interval_of_shoot = 5, time_to_stop = 480.0, wait_time = 50):
	axis = -Vector3.UnitY if task.ExecutedCount % 2 == 0 else Vector3.UnitY

	root = EntityShot(WORLD, "BONE", 0xFFFFFF)
	root.LifeSpan = time_to_stop + wait_time
	root.GetRecordedRot = lambda e: e.Rot
	root.Pos = CENTER_BONE.WorldPos + Vector3(0, 0, -300)
	root.Rot = Quaternion.RotationAxis(Vector3.UnitY, RAD * 180)

	def record(): root.AddRootBoneKeyFrame()
	root.AddTask(record, 0, 1, wait_time)

	def rotate_root(rot = Quaternion.RotationAxis(axis, RAD * 360.0 / (time_to_stop / interval_of_shoot))): root.Rot *= rot
	root.AddTask(rotate_root, interval_of_shoot, time_to_stop / interval_of_shoot, wait_time + interval_of_shoot)
	root.Spawn()

	parent = EntityShot(WORLD, "BONE", 0xFFFFFF, root)
	parent.LifeSpan = root.LifeSpan
	parent.GetRecordedRot = lambda e: e.Rot
	parent.Rot = Quaternion.RotationAxis(Vector3.UnitY, RAD * 180)
	parent.Velocity = Vector3(0.4, 0, 0)

	def record(): parent.AddRootBoneKeyFrame()
	parent.AddTask(record, 0, 1, wait_time)

	def rotate_parent(rot = Quaternion.RotationAxis(axis, RAD * -45.0 / (time_to_stop / interval_of_shoot))): parent.Rot *= rot
	parent.AddTask(rotate_parent, interval_of_shoot, time_to_stop / interval_of_shoot, wait_time + interval_of_shoot)
	parent.Spawn()

	def shot_dia(ignore_vec = Vector3.UnitZ):
		for vec in veclist:
			if vec * ignore_vec < -0.75: continue

			shot = EntityShotStraight(WORLD, "DIA_BRIGHT", 0x400000)
			shot.Pos = parent.WorldPos
			shot.Velocity = vec * parent.WorldRot * 12.0
			shot.LifeSpan = 100
			shot.Spawn()
	parent.AddTask(shot_dia, interval_of_shoot, 0, 0)

	def shot_laser():
		for vec in laser_veclist:
			laser = EntityShot(WORLD, "LASER_LINE", 0x0000A0, Vector3(2, 2, 4000))
			laser.Parent = parent
			laser.GetRecordedRot = lambda e: e.Rot
			laser.Rot = Matrix3.LookAt(vec, Vector3.UnitY)
			laser.LifeSpan = time_to_stop + wait_time - 30

			morph = laser.CreateVertexMorph(0, lambda v: Vector3(v.x * -0.99, v.y * -0.99, 0))
			laser.AddMorphKeyFrame(morph, 1, 0)
			laser.AddMorphKeyFrame(morph, 1, 20)
			laser.AddMorphKeyFrame(morph, 0, 50)
			laser.AddMorphKeyFrame(morph, 0, laser.LifeSpan - 30)
			laser.AddMorphKeyFrame(morph, 1, laser.LifeSpan)

			laser.Spawn()
	parent.AddTask(shot_laser, 0, 1, 0)
WORLD.AddTask(laser_and_dia_task, 600, 2, 0, True)

def shoot_dia_while_rotating(vec, axis):
	if abs(vec * axis) > 0.99: return

	axis = cross3(vec, vec, axis)

	def shot_dia(task, vec_ = [vec], rot = Quaternion.RotationAxis(axis, RAD * 0.6)):
		if task.ExecutedCount % 8 < 4:
			for i in range(2):
				shot = EntityShotStraight(WORLD_SUB, "DIA", 0x0000A0)
				shot.Pos = Vector3(0, 0, 0)
				shot.Velocity = vec_[0] * (i + 1) * 2.0
				shot.LifeSpan = 240 * (2 - i)
				shot.Spawn()
		vec_[0] *= rot * rot
	WORLD.AddTask(shot_dia, 1, 960, 60, True)

for vec in objvertices("ico.obj", 1):
	for axis in Vector3.UnitX, Vector3.UnitY, Vector3.UnitZ:
		shoot_dia_while_rotating(vec, -axis)
