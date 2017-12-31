# -*- coding: utf-8 -*-

interval = 4

vecList = []
objvertices("ico.obj", lambda v: vecList.append(+v))

angleList = [RAD, -RAD]
axisList = [Vector3.UnitX, Vector3.UnitZ]

def world_task(axis, angle, range, should_shot_scale):
	for vec in vecList:
		if (vec ^ axis).Length() < 0.01: continue
		
		rotateAngle = 4
		rotateQuat = Quaternion.RotationAxis(vec ^ (vec ^ axis), angle * rotateAngle)
		
		root = EntityShot(WORLD, BONE, 0xFFFFFF)
		root.Recording = Recording.LocalMat
		root.Pos = OWNER_BONE.WorldPos
		root.Rot =  rotateQuat ^ (90 / rotateAngle)
		
		def rotate_root(root = root, rotateQuat = rotateQuat): root.Rot *= rotateQuat
		root.AddTask(rotate_root, interval, 0, 0)
		root()
		
		parent = EntityShot(WORLD, MAGIC_CIRCLE, 0xFFFFFF, root)
		parent.Recording = Recording.LocalMat
		parent.Pos = vec * range
		
		if parent.ModelData.OwnerEntities.Count == 1:
			for vert in parent.ModelData.Vertices: vert.Pos *= 4
		
		parent.Rot = Quaternion.RotationAxis(Vector3.UnitZ ^ vec, math.acos(vec.z))
		
		rotateQuat = rotateQuat ^ 2
		
		def shot_dia(task, parent = parent, rotateQuat = rotateQuat):
			parent.Rot *= rotateQuat
			
			shot = EntityShot(WORLD, DIA, 0xFFA0FF)
			shot.Pos = parent.WorldPos
			shot.Velocity = Vector3.UnitZ * parent.WorldMat * -2.4
			shot()
			
			if task.RunCount % 2 == 0:
				def reverse(shot = shot, parent = parent):
					shot.Velocity *= -10
				shot.AddTask(reverse, 0, 1, 110)
		parent.AddTask(shot_dia, interval, int(300 / interval), 0, True)
		
		if should_shot_scale:
			def shot_scale(task, root = root, parent = parent, mat = Matrix3.RotationAxis(Vector3.UnitY, RAD * 90)):
				target = Vector3(0, 0, 1024)
				sidevec = +(target - root.WorldPos) * mat
				targetPosList = [target - sidevec * 20, target, target + sidevec * 20]
				
				for targetPos in targetPosList:
					shot = EntityShot(WORLD, SCALE, 0xA00000 if task.RunCount % 2 == 0 else 0xA000A0)
					shot.Velocity = +(targetPos - parent.WorldPos) * 20
					shot.Upward = Vector3.UnitY * parent.WorldMat
					shot.Pos = parent.WorldPos
					shot()
			parent.AddTask(shot_scale, interval, int(80 / interval), 220, True)
		parent()
WORLD.AddTask(lambda: world_task(Vector3.UnitX, RAD, 512, False), 0, 1, 0)
WORLD.AddTask(lambda: world_task(Vector3.UnitX, -RAD, 512, False), 0, 1, 0)
WORLD.AddTask(lambda: world_task(Vector3.UnitZ, RAD, 512, True), 0, 1, 0)
WORLD.AddTask(lambda: world_task(Vector3.UnitZ, -RAD, 512, True), 0, 1, 0)
