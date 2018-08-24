# -*- coding: utf-8 -*-
import MMDataIO.Pmx

import pickle
with open(EXPORT_DIRECTORY + '\\poslist.pickle', mode='rb') as f:
	from VecMath.Geometry import Sphere
	poslist = pickle.load(f)
	sp_list = [Sphere(p, 24) for p, n in poslist]
	pl_list = [Plane(p, n) for p, n in poslist]

def particle_task(sender, e):
	for i in range(15):
		particle = EntityShot(WORLD, "S", sender.Property.Color, randint(1, 3) * 0.1)
		particle.Pos = sender.Pos + randomvec() * 1
		particle.Velocity = randomvec() * 0.5
		particle.LifeSpan = randint(15, 25)
		
		"""uv_morph = particle.CreateUvMorph(0, MMDataIO.Pmx.MorphType.EXUV2, lambda p: Vector4(-1, -1, 0, 0))
		particle.AddMorphKeyFrame(uv_morph, 0, 0)
		particle.AddMorphKeyFrame(uv_morph, 1, particle.LifeSpan)"""
		
		vtx_morph = particle.CreateVertexMorph(1, lambda v: -v)
		particle.AddMorphKeyFrame(vtx_morph, 0, 0)
		particle.AddMorphKeyFrame(vtx_morph, 1, particle.LifeSpan)
		
		particle.Spawn()

def shot_red_amullet():
	if abs(REIMU_SHOT_FLAG.Pos.y) < 0.01: return
	
	def calc_time_to_interesect(plane, pos, velocity, r):
		t = plane.CalculateTimeToIntersectWithRay(pos, velocity)
		return t if (pos + velocity * t - plane.Pos).LengthSquare() < r ** 2 else 1E7
	
	hand_mat = OPTION_CENTER_BONE.LocalMat
	
	for bone in OPTION_BALL_BONES:
		mat = bone.WorldMat
		
		for i in range(randint(1, 3)):
			shot = EntityShot(WORLD, "AMULET", 0xFF0000, 0.4)
			shot.Pos = mat.Translation
			shot.Velocity = Vector3.UnitZ * hand_mat * Matrix3.RotationAxis(randomvec(), RAD * 10) * 16 * REIMU_SHOT_FLAG.Pos.y
			shot.Upward = randomvec()
			shot.LifeSpan = min(200, min([abs(calc_time_to_interesect(pl, shot.Pos, shot.Velocity, 100)) for pl in pl_list]))
			shot.RemovedEvent += particle_task
			shot.Spawn()
WORLD.AddTask(shot_red_amullet, 0, 0, 0)

def shot_homing_amulet_ex(speed = 24):
	if abs(REIMU_SHOT_FLAG.Pos.z) < 0.01: return
	
	hand_mat = OPTION_CENTER_BONE.LocalMat
	
	for bone in OPTION_BALL_BONES:
		mat = bone.WorldMat
		
		for i in range(randint(1, 2)):
			shot = EntityShot(WORLD, "AMULET", 0xFF00FF, 0.6)
			shot.Pos = mat.Translation
			shot.Velocity = Vector3.UnitZ * hand_mat * Matrix3.RotationAxis(randomvec(), RAD * 40) * speed * REIMU_SHOT_FLAG.Pos.z
			shot.Upward = randomvec()
			
			def particle_task(shot = shot):
				for i in range(3):
					particle = EntityShot(WORLD, "S", 0xFF00FF, randint(1, 3) * 0.1)
					particle.Pos = shot.Pos + randomvec() * 1 - shot.Velocity * random()
					particle.Velocity = randomvec() * 0.5
					particle.LifeSpan = randint(15, 25)
					
					uv_morph = particle.CreateUvMorph(0, MMDataIO.Pmx.MorphType.EXUV2, lambda p: Vector4(-1, -1, 0, 0))
					particle.AddMorphKeyFrame(uv_morph, 0, 0)
					particle.AddMorphKeyFrame(uv_morph, 1, particle.LifeSpan)
					
					particle.Spawn()
			#shot.AddTask(particle_task, 0, 0, 0)
			
			def homing(shot = shot):
				vec_to_target = CENTER_BONE.WorldPos - shot.Pos
				vec_to_target_normalized = +vec_to_target
				vec = +shot.Velocity
				
				intersect_sp_list = [sp for sp in sp_list if sp.IsIntersectWithRay(shot.Pos, shot.Velocity) and (sp.Pos - shot.Pos).LengthSquare() < 160000]
				
				if len(intersect_sp_list):
					sp = min(intersect_sp_list, key = lambda s: (s.Pos - shot.Pos).LengthSquare())
					
					if (sp.Pos - shot.Pos).LengthSquare() < sp.Range ** 2:
						shot.LifeSpan = 1
						return
						
					vec_to_sp = sp.Pos - shot.Pos
					
					length_to_sp = vec_to_sp.Length()
					dot2 = sp.Range ** 2 - length_to_sp ** 2 + (vec * vec_to_sp) ** 2
					cos = math.sqrt(dot2) / length_to_sp
					
					alpha = (1 - cos) * 0.2
					shot.Velocity = vec * Matrix3.RotationAxis(vec_to_target ^ shot.Velocity, math.acos(cos) * alpha) * speed
				else:
					alpha = (1 - vec * vec_to_target_normalized) * 0.6
					
					shot.Velocity = (vec + (vec_to_target_normalized - vec) * alpha) * speed
					shot.LifeSpan = shot.FrameCount + int((CENTER_BONE.WorldPos - shot.Pos).Length() / (speed * alpha * 2.5))
			shot.AddTask(homing, 0, 0, 0)
			shot.Spawn()
WORLD.AddTask(shot_homing_amulet_ex, 0, 0, 0)
