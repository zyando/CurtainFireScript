# -*- coding: utf-8 -*-

def create_veclist(path):
	return objvertices(path[0] + ".obj", path[1])
path_list = ("ico", 0), ("ico", 1), ("ico", 2), ("dod", 0), ("ico_dod", 0), ("snub_cube", 0), ("beveled_snub_cube", 0)
vec_dict = {path[0] + ("" if path[1] == 0 else str(path[1])) : create_veclist(path) for path in path_list}

def world_task():
	def shot_laser():
		for vec in vec_dict["ico1"]:
			flag = vec in vec_dict["ico"]
			shot = EntityShot(WORLD, "LASER", 0xA000A0 if flag else 0x0000A0, Matrix4(Matrix3(80, 80, 1000), Vector3(0, 0, -24)))
			
			morph = shot.CreateVertexMorph(0, lambda v: Vector3(-v.x * 0.9, -v.y * 0.9, 0))
			shot.AddMorphKeyFrame(morph, 1, 0)
			shot.AddMorphKeyFrame(morph, 1, 69)
			shot.AddMorphKeyFrame(morph, 0, 70)
			shot.AddMorphKeyFrame(morph, 0, 180)
			shot.AddMorphKeyFrame(morph, 1, 200)
			shot.LifeSpan = 200
			
			shot.GetRecordedRot = lambda e: e.Rot
			shot.Pos = CENTER_BONE.WorldPos
			
			rot = Matrix3.LookAt(vec, Vector3.UnitY)
			shot.Rot = rot * Matrix3.RotationAxis(vec ^ (vec ^ Vector3.UnitY), RAD * (170 if flag else -170))
			def set_rotation(shot = shot, rot = rot):
				shot.Rot = rot
			shot.AddTask(set_rotation, 0, 1, 50)
			shot.Spawn()
	WORLD.AddTask(shot_laser, 0, 1, 0)
	
	def shot_l():
		for vec in vec_dict["beveled_snub_cube"]:
			shot = EntityShot(WORLD, "L", 0xFF4040)
			shot.Velocity = vec * 2
			shot.Pos = CENTER_BONE.WorldPos + +shot.Velocity * 20
			shot.LifeSpan = 400
			
			def divide_shot(shot = shot):
				for i in range(3):
					new_shot = EntityShot(WORLD, shot.Property)
					new_shot.Velocity = shot.Velocity * (1 + i) * 3
					new_shot.Pos = shot.Pos
					new_shot.LifeSpan = 200
					new_shot.Spawn()
			shot.AddTask(divide_shot, 0, 1, 40)
			shot.Spawn()
	WORLD.AddTask(shot_l, 0, 1, 200)
	
	def shot_butterfly_gb():
		for vec in vec_dict["beveled_snub_cube"] +  vec_dict["snub_cube"]:
			flag = vec in vec_dict["snub_cube"]
			
			for i in range(3 if flag else 2):
				shot = EntityShot(WORLD, "BUTTERFLY", 0x0000A0 if flag else 0xA000A0)
				shot.Velocity = vec * (1 + i * 0.6)
				shot.Pos = CENTER_BONE.WorldPos + +shot.Velocity * 20
				shot.LifeSpan = 400 - i * 50
				
				def divide_shot(shot = shot):
					for i in range(3):
						new_shot = EntityShot(WORLD, shot.Property)
						new_shot.Velocity = shot.Velocity * -(1 + i * 0.4) * 3
						new_shot.Pos = shot.WorldPos
						new_shot.SetMotionInterpolationCurve(Vector2(0.2, 0.5), Vector2(0.9, 0.045), 200)
						new_shot.LifeSpan = 300
						new_shot.Spawn()
					
					for i in range(3):
						new_shot = EntityShot(WORLD, shot.Property)
						new_shot.Velocity = shot.Velocity * (1 + i) * 3
						new_shot.Pos = shot.WorldPos
						new_shot.LifeSpan = 300
						new_shot.Spawn()
				shot.AddTask(divide_shot, 0, 1, 60 - i * 5)
				shot.Spawn()
	WORLD.AddTask(shot_butterfly_gb, 0, 1, 0)
	
	def shot_butterfly_r(task):
		parentShot = EntityShot(WORLD, "BONE", 0xFFFFFF)
		parentShot.GetRecordedRot = lambda e: e.Rot
		parentShot.Pos = CENTER_BONE.WorldPos
		
		quat = Quaternion.RotationAxis(Vector3.UnitY, RAD * 60  * (1 if task.ExecutedCount % 2 == 0 else -1))
		
		def rotate():
			parentShot.Rot *= quat
		parentShot.AddTask(rotate, 0, 1, 120)
		parentShot()
		
		for vec in vec_dict["ico2"]:
			if vec in vec_dict["ico1"]: continue
			
			for i in range(2):
				shot = EntityShot(WORLD, "BUTTERFLY", 0xA00000, parentShot)
				shot.Velocity = vec * (1 + i * 0.6)
				shot.Pos = +shot.Velocity * 20
				
				wait_frame = 120 - i * 5
				
				def divide_shot(shot = shot, rot = quat ^ (120.0 / wait_frame)):
					shotVec = shot.Velocity *  shot.ParentEntity.Rot
					
					for i in range(3):
						new_shot = EntityShot(WORLD, shot.Property)
						new_shot.Velocity = shotVec * -(1 + i * 0.4) * 3
						new_shot.Pos = shot.WorldPos
						new_shot.SetMotionInterpolationCurve(Vector2(0.2, 0.5), Vector2(0.9, 0.045), 200)
						new_shot.LifeSpan = 400
						new_shot.Spawn()
					
					for i in range(3):
						new_shot = EntityShot(WORLD, shot.Property)
						new_shot.Velocity = shotVec * (1 + i) * 3
						new_shot.Pos = shot.WorldPos
						new_shot.LifeSpan = 200
						new_shot.Spawn()
				shot.AddTask(divide_shot, 0, 1, wait_frame)
				shot.LifeSpan = 400
				shot.Spawn()
	WORLD.AddTask(shot_butterfly_r, 15, 4, 60, True)
WORLD.AddTask(world_task, 240, 2, 0)
