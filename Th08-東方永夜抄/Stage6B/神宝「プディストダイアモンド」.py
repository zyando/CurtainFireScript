# -*- coding: utf-8 -*-

veclist = []

z_mat = Matrix3.RotationZ(pi * 0.5)

for vec in objvertices("beveled_snub_cube.obj", 0) + [Vector3.UnitZ]:
	for r in range(3):
		v = Vector3.Interpolate(vec, Vector3.UnitZ, r * 0.3)
		if v.z < cos(math.pi * 0.4): continue
		
		veclist.append(v * z_mat * (1 + r) * 160)

for vec in veclist:
	vec *= HAND_BONE.WorldRot
	
	parent = EntityShot(WORLD, "MAGIC_CIRCLE", 0x000040, 4)
	parent.Pos = CENTER_BONE.WorldPos
	parent.Velocity = vec * (1.0 / 15)
	
	def pause(p = parent):
		p.Velocity *= 0
	parent.AddTask(pause, 0, 1, 15)
	
	def shot_laser(task, parent = parent, vec = normalize(vec)):
		if task.ExecutedCount > 0: vec = vec * Matrix3.RotationAxis(cross(vec, randomvec()), RAD * random() * 60)
		
		laser = EntityShot(WORLD, "LASER_LINE", 0x0000A0, Vector3(3, 3, 4000))
		laser.GetRecordedRot = lambda e: e.Rot
		laser.Pos = parent.Pos
		laser.Rot = Matrix3.LookAt(vec, Vector3.UnitZ)
		laser.LifeSpan = 140
		
		laser.Spawn()

		morph = laser.CreateVertexMorph(0, lambda v: Vector3(-v.x * 0.9, -v.y * 0.9, 0))
		laser.AddMorphKeyFrame(morph, 1, 0)
		laser.AddMorphKeyFrame(morph, 1, 29)
		laser.AddMorphKeyFrame(morph, 0, 30)
		laser.AddMorphKeyFrame(morph, 0, 120)
		laser.AddMorphKeyFrame(morph, 1, 140)
	parent.AddTask(shot_laser, 120, 0, 15, True)
	parent.Spawn()

	parent.SetMotionInterpolationCurve(Vector2(0.2, 0.8), Vector2(0.2, 0.8), 15)

def shot_star():
	for i in range(16):
		shot = EntityShot(WORLD, "STAR_S", 0xA00000)
		shot.Pos = Vector4(gauss(0, 1) * 600, gauss(0, 1) * 400, gauss(40, 40), 1) * HAND_BONE.WorldMat
		shot.Velocity = Vector3.UnitZ * Matrix3.RotationAxis(cross(Vector3.UnitZ, randomvec()), RAD * random() * 60) * HAND_BONE.WorldRot * uniform(4, 8)
		shot.LifeSpan = 450
		shot.Spawn()
WORLD.AddTask(shot_star, 0, 0, 30)

def shot_blue_scale():
	for i in range(8):
		shot = EntityShot(WORLD, "SCALE", 0x0000A0)
		shot.Pos = HAND_BONE.WorldPos
		shot.Velocity = normalize(REIMU_CENTER_BONE.WorldPos - shot.Pos) * (i * 0.8 + 6)
		shot.LifeSpan = 120
		shot.Spawn()
WORLD.AddTask(shot_blue_scale, 45, 0, 90)
