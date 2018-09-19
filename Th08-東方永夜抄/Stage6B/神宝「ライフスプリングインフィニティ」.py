# -*- coding: utf-8 -*-

obj = WavefrontObject("ico.obj").divide(1)
facelist = [[+obj.veclist[i] for i in face] for face in obj.face_index_list]

ico0_veclist = objvertices("ico.obj", 0)
ico4_veclist = objvertices("ico.obj", 4)

def task():
	vec_to_target = TARGET_BONE.WorldPos - CENTER_BONE.WorldPos + randomvec() * gauss(0, 200)
	
	for vec in ico4_veclist:
		if vec * normalize(vec)_to_target > 0.7: continue
		
		for speed in 4, 6:
			shot = EntityShot(WORLD, "S", 0xA00000)
			shot.Pos = CENTER_BONE.WorldPos
			shot.Velocity = vec * speed
			shot.LifeSpan =  200
			shot.Spawn()
	
	parent = EntityShot(WORLD, "BONE", 0)
	parent.Pos = CENTER_BONE.WorldPos
	parent.Velocity = normalize(vec_to_target) * 12
	parent.LifeSpan = 75
	parent.SetMotionInterpolationCurve(Vector2(0.2, 0.8), Vector2(0.2, 0.8), 30)
	
	def stop(): parent.Velocity *= 0
	parent.AddTask(stop, 0, 1, 30)
	parent.Spawn()
	
	for vec in ico0_veclist:
		mgc = EntityShot(WORLD, "MAGIC_CIRCLE", 0x200050, 10)
		mgc.Parent = parent
		mgc.LifeSpan = parent.LifeSpan
		mgc.LookAtVec = vec
		
		morph = mgc.CreateVertexMorph(0, lambda v: -v)
		mgc.AddMorphKeyFrame(morph, 1, 0)
		mgc.AddMorphKeyFrame(morph, 0, 15)
		mgc.Spawn()
	
	def shot_laser(face, veclist = [Vector3.UnitY * Matrix3.RotationZ(math.pi * 2 / 16 * i) for i in range(32)]):
		center = (face[0] + face[1] + face[2]) * (1.0 / 3)
		
		for vtx in face:
			for i in 1, -1:
				shot = EntityShot(WORLD, "LASER_LINE", 0xA000A0 if i > 0 else 0x00A0A0, Vector3(2, 2, 4000))
				shot.Pos = parent.Pos + center * 120
				shot.LookAtVec = normalize(vtx - center) * i
				shot.LifeSpan = parent.LifeSpan
				
				morph = shot.CreateVertexMorph(0, lambda v: Vector3(-v.x * 0.9, -v.y * 0.9, 0))
				shot.AddMorphKeyFrame(morph, 1, 0)
				shot.AddMorphKeyFrame(morph, 1, 14)
				shot.AddMorphKeyFrame(morph, 0, 15)
				shot.AddMorphKeyFrame(morph, 0, 45)
				shot.AddMorphKeyFrame(morph, 1, 75)
				shot.Spawn()
		
		def shot_star():
			mat = Matrix3.LookAt(center, randomvec())
			
			for vec in veclist:
				shot = EntityShot(WORLD, "STAR_S", 0xA00000)
				shot.Pos = parent.Pos
				shot.Velocity = vec * mat * 2
				shot.LifeSpan = 400
				shot.SetMotionInterpolationCurve(Vector2(0.3, 0.7), Vector2(0.3, 0.7), 45, False)
				
				def curve(shot = shot, rot = Matrix3.RotationAxis(center, RAD * 2)): shot.Velocity *= rot
				shot.AddTask(curve, 0, 30, 45)
				
				shot.Spawn()
		WORLD.AddTask(shot_star, 0, 1, 30)
	WORLD.AddTask(lambda: [shot_laser(face) for face in facelist], 0, 1, 30)
WORLD.AddTask(task, 150, 4, 0)
