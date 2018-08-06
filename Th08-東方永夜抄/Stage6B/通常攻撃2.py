# -*- coding: utf-8 -*-
veclist = []

z_mat = Matrix3.RotationZ(pi * 0.5)

for vec in objvertices("ico.obj", 1):
	for r in range(3):
		v = Vector3.Interpolate(vec, Vector3.UnitZ, r * 0.3)
		if v.z < cos(math.pi * 0.4): continue
		
		veclist.append(v * z_mat * (1 + r) * 160)

for vec in objvertices("ico.obj", 0):
	for r in range(3):
		v = Vector3.Interpolate(vec, Vector3.UnitZ, (r + 1) * 0.2)
		if v.z < cos(math.pi * 0.4): continue
		
		veclist.append(v * (0.5 + r) * 160)
		
poslist = []

def particle_task(sender, e):
	for i in range(30):
		particle = EntityShot(WORLD, "S", sender.Property.Color, randint(1, 3) * 0.5)
		particle.Pos = sender.Pos + randomvec() * 5
		particle.Velocity = randomvec() * 2
		particle.LifeSpan = randint(15, 25)
		
		vtx_morph = particle.CreateVertexMorph(1, lambda v: -v)
		particle.AddMorphKeyFrame(vtx_morph, 0, 0)
		particle.AddMorphKeyFrame(vtx_morph, 1, particle.LifeSpan)
		particle()

for vec in veclist:
	parent = EntityShot(WORLD, "MAGIC_CIRCLE", 0x000040, 5)
	parent.LifeSpan = 1540 - WORLD.StartFrame + randint(0, 10)
	parent.RemovedEvent += particle_task
	parent.Pos = CENTER_BONE.WorldPos
	parent.Velocity = vec * (1.0 / 30) * HAND_BONE.WorldRot
	parent.SetMotionInterpolationCurve(Vector2(0.2, 0.8), Vector2(0.2, 0.8), 30)
	
	def pause(p = parent):
		poslist.append((p.Pos, +parent.Velocity))
		p.Velocity *= 0
	parent.AddTask(pause, 0, 1, 30)
	
	def shot_s(parent = parent, vec = +vec, binder = [Vector3.UnitZ, Matrix3.RotationY(RAD * 10)]):
		shot = EntityShot(WORLD, "S", 0x0000A0)
		shot.Pos = parent.Pos + randomvec() * gauss(0, 80)
		
		for i in range(3):
			shot.Pos[i] -= shot.Pos[i] % 3
		shot.LifeSpan = 300
		shot()
		
		def move(v = binder[0] * Matrix3.RotationAxis(randomvec(), RAD * 90 * gauss()) * 5):
			shot.Velocity = v
		shot.AddTask(move, 0, 1, 60)
		
		binder[0] *= binder[1]
	parent.AddTask(shot_s, 10, 64, 75 + randint(0, 10))
	parent()

def export_poslist():
	import pickle
	with open(EXPORT_DIRECTORY + '\\poslist.pickle', mode='wb') as f:
		pickle.dump(poslist, f)
WORLD.AddTask(export_poslist, 0, 1, 40)
