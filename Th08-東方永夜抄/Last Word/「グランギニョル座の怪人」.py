# -*- coding: utf-8 -*-

def world_task(vec, axis, angle1, angle2, range, should_shot_scale):
	root = EntityShot(WORLD, "BONE", 0)
	root.GetRecordedRot = lambda e: e.Rot
	root.Pos = CENTER_BONE.WorldPos
	root()
	
	parent = EntityShot(WORLD, "MAGIC_CIRCLE", 0xFFFFFF, root)
	parent.GetRecordedRot = lambda e: e.Rot
	parent.Pos = vec * range
	parent.Rot = Matrix3.LookAt(vec, randomvec())
	parent()
	
	rot1 = Quaternion.RotationAxis(axis, angle1)
	rot2 = Quaternion.RotationAxis(axis, angle2)
	
	def shot_dia(task):
		root.Rot *= rot1
		parent.Rot *= rot2
		
		shot = EntityShot(WORLD, "DIA", 0xA0A0A0)
		shot.Pos = parent.WorldPos
		shot.Velocity = -Vector3.UnitZ * parent.WorldMat * 2
		shot.LivingLimit = 400
		shot()
		
		if task.ExecutedCount % 2 == 0:
			def pause(): shot.Velocity *= 0
			shot.AddTask(pause, 0, 1, 120)
			
			def turn(): shot.Velocity = shot.LookAtVec * (rot2 ^ 8) * -8
			shot.AddTask(turn, 0, 1, 180)
			
	root.AddTask(shot_dia, 2, 400, 0, True)
	
	if should_shot_scale:
		poslist = [Vector3(20, 0, 0), Vector3.Zero, Vector3(-20, 0, 0)]
		
		def shot_scale(task):
			for pos in poslist:
				shot = EntityShotStraight(WORLD, "SCALE", 0xA00000 if task.ExecutedCount % 2 == 0 else 0xA000A0)
				shot.Pos = parent.WorldPos
				shot.Velocity = +(vec3(vec4(pos) * TARGET_BONE.WorldMat) - shot.Pos) * 12
				shot.LivingLimit = 80
				shot()
		root.AddTask(shot_scale, 2, 50, 240, True)

for vec in objvertices("ico.obj", 0):
	for axis in Vector3.UnitX, Vector3.UnitZ:
		if vec * axis > 0.95: continue
		
		for i in 1, -1:
			world_task(vec, vec ^ (vec ^ axis) * i, RAD * 1, RAD * 4, 128, axis.z == i)
