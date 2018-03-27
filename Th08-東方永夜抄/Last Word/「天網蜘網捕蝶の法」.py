# -*- coding: utf-8 -*-

def shot_func(pos, vec, way, level):
	shot = EntityShot(WORLD, "S", 0x0000A0, 3)
	shot.Pos = pos
	shot.Velocity = vec * 100
	shot.LivingLimit = 50
	shot()
	
	laser = EntityShot(WORLD, "LASER_LINE", 0x0000A0, Vector3(2, 2, 4000))
	
	laser.Pos = pos
	laser.LookAtVec = vec
	
	morph = laser.CreateVertexMorph(lambda v: Vector3(-v.x * 0.9, -v.y * 0.9, 0))
	laser.AddMorphKeyFrame(morph, 1, 0)
	laser.AddMorphKeyFrame(morph, 1, 29)
	laser.AddMorphKeyFrame(morph, 0, 30)
	laser.AddMorphKeyFrame(morph, 0, 100)
	laser.AddMorphKeyFrame(morph, 1, 120)
	
	laser.LivingLimit = 120
	laser()
	
	if level < 0: return
	
	def shot_task_func():
		mat1 = Matrix3.RotationAxis(+(vec ^ Vector3.UnitY), RAD * 60)
		mat2 = Matrix3.RotationAxis(vec, RAD * (360 / way))
		shotVec = vec * mat1
		
		for i in range(way):
			shot_func(shot.Pos, +shotVec, way, level - 1)
			shotVec = shotVec * mat2
	shot.AddTask(shot_task_func, 0, 1, 6)
	shot.LivingLimit = 10
	
	fixed_shot = EntityShot(WORLD, "M", 0x0000A0)
	fixed_shot.Pos = pos
	fixed_shot.LivingLimit = laser.LivingLimit
	
	def shot_m():
		for i in range(2):
			shot = EntityShot(WORLD, "M", 0x0000A0)
			shot.Pos = pos
			shot.LivingLimit = 500
			shot.Velocity = Vector3.UnitZ  * (i * 2 - 1) * 4
			shot()
	fixed_shot.AddTask(shot_m, 0, 1, 50)
	fixed_shot()
way_and_level_list = (3, 4), (4, 4), (3, 5), (4, 4), (6, 3), (4, 5)
def get_way_and_level(i): return way_and_level_list[i % len(way_and_level_list)]

WORLD.AddTask(lambda t: shot_func(CENTER_BONE.WorldPos, -Vector3.UnitZ, *get_way_and_level(t.ExecutedCount)), 150, 6, 10, True)
