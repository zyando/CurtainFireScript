# -*- coding: utf-8 -*-

num_shot = 80
interval = 5

target = Vector3(0, 0, 80)

veclist = objvertices("ico.obj", 1)

laser_veclist = []

way = 8
mat = Matrix3.RotationAxis(Vector3.UnitZ, RAD * (360 / way))
vec = Vector3.UnitY

for i in range(way):
	laser_veclist.append(vec)
	vec = vec * mat

def world_task():
	rot = Matrix3.RotationAxis(randomvec(), RAD * 20)
	
	for vec in laser_veclist:
		axis = cross(vec, Vector3.UnitZ) * rot
		shotrot = Quaternion.RotationAxis(axis, RAD * 45)
		front = Vector3.UnitZ * rot
		vec = vec * rot
		
		for i in range(2):
			shot = EntityShot(WORLD, "LASER_LINE", 0xA00000, Vector3(6, 6, 4000))
			shot.GetRecordedRot = lambda e: e.Rot
			shot.Rot = Matrix3.LookAt(vec, front)
			shot.Pos = CENTER_BONE.WorldPos + vec * 80
			
			def add_keyframe(shot = shot):
				shot.AddRootBoneKeyFrame()
			shot.AddTask(add_keyframe, 0, 1, 39)
			
			def rotate(shot = shot, shotrot = shotrot):
				shot.Rot *= shotrot
			shot.AddTask(rotate, 6, 2, 40)
			
			morph = shot.CreateVertexMorph(0, lambda v: Vector3(-v.x * 0.9, -v.y * 0.9, 0))
			shot.AddMorphKeyFrame(morph, 1, 0)
			shot.AddMorphKeyFrame(morph, 1, 20)
			shot.AddMorphKeyFrame(morph, 0, 30)
			shot.AddMorphKeyFrame(morph, 0, 120)
			shot.Spawn()
			
			shotrot = ~shotrot
			
			if i == 0:
				def shot_task(task, r1, r2, axis, front, shot, numshot = 30):
					root = Entity(WORLD)
					root.Pos = shot.Pos + front * (r1 * (-1 + task.ExecutedCount * 2))
					root.Spawn()
					
					def rotate(r = Quaternion.RotationAxis(axis, RAD * (180 / numshot))):
						root.Rot *= r
					WORLD.AddTask(rotate, 1, numshot, 0)
					
					parent = Entity(WORLD, root)
					parent.Pos = front * -r2
					parent.Rot = Quaternion.RotationAxis(axis, RAD * 60)
					parent.Spawn()
					
					def shot_dia():
						vec = front * parent.WorldMat
						
						shot = EntityShot(WORLD, "DIA", 0xA00000)
						shot.Pos = parent.WorldPos
						shot.LookAtVec = vec
						
						def move():
							shot.Velocity = vec * 2.4
						shot.AddTask(move, 0, 1, 100)
						shot.Spawn()
					WORLD.AddTask(shot_dia, 1, numshot, 0)
				WORLD.AddTask(lambda t, a = axis, f = front, s = shot: shot_task(t, 80, 80, a, f, s), 30, 3, 40, True)
				WORLD.AddTask(lambda t, a = axis, f = front, s = shot: shot_task(t, 85, 90, a, f, s), 30, 3, 70, True)
				WORLD.AddTask(lambda t, a = axis, f = front, s = shot: shot_task(t, 75, 85, a, f, s), 30, 3, 100, True)
	
	for vec in veclist:
		for axis in [Vector3.UnitX]:
			axis = cross3(vec, vec, axis)
			rot = Matrix3.RotationAxis(axis, RAD * 12)
			
			def shot_s(task, vec = vec, rot = rot):
				rot = rot if task.ExecutedCount % 2 == 0 else ~rot
				shotvec = vec
				
				for i in range(5):
					shotvec = shotvec * rot
					
					shot = EntityShot(WORLD, "S", 0x0000A0)
					shot.Pos = CENTER_BONE.WorldPos
					shot.Velocity = shotvec * 3.0 * (1 + i * 0.2) * 2
					shot.LifeSpan = 100
					shot.Spawn()
			WORLD.AddTask(shot_s, 10, 30, 30, True)
WORLD.AddTask(world_task, 0, 1, 0)
