# -*- coding: utf-8 -*-

def shot_func(pos, vec, way, level):
	shot = EntityShot(WORLD, "M", 0x0000A0)
	shot.Pos = pos
	shot.Velocity = vec * 100
	shot.LifeSpan = 50
	shot.Spawn()
	
	laser = EntityShot(WORLD, "LASER_LINE", 0x0000A0, Vector3(2, 2, 4000))
	
	laser.Pos = pos
	laser.LookAtVec = vec
	
	morph = laser.CreateVertexMorph(0, lambda v: Vector3(-v.x * 0.9, -v.y * 0.9, 0))
	laser.AddMorphKeyFrame(morph, 1, 0)
	laser.AddMorphKeyFrame(morph, 1, 29)
	laser.AddMorphKeyFrame(morph, 0, 30)
	laser.AddMorphKeyFrame(morph, 0, 100)
	laser.AddMorphKeyFrame(morph, 1, 120)
	
	laser.LifeSpan = 120
	laser.Spawn()
	
	if level < 0: return
	
	def shot_task_func():
		mat1 = Matrix3.RotationAxis(+(vec ^ Vector3.UnitY), RAD * 60)
		mat2 = Matrix3.RotationAxis(vec, RAD * (360 / way))
		shotVec = vec * mat1
		
		for i in range(way):
			shot_func(shot.Pos, +shotVec, way, level - 1)
			shotVec = shotVec * mat2
	shot.AddTask(shot_task_func, 0, 1, 6)
	shot.LifeSpan = 10
	
	def shot_m():
		for i in range(2):
			shot = EntityShotStraight(WORLD, "M", 0x0000A0)
			shot.Pos = pos
			shot.LifeSpan = 500
			shot.Velocity = Vector3.UnitZ  * (i * 2 - 1) * 4
			shot.Spawn()
	WORLD.AddTask(shot_m, 0, 1, 50)
way_and_level_list = list(reversed([(3, 5), (4, 5), (3, 6), (4, 5), (5, 4), (6, 4)]))

WORLD.AddTask(lambda: shot_func(CENTER_BONE.WorldPos, -Vector3.UnitZ, *way_and_level_list.pop()), 150, 6, 10)
