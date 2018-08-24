# -*- coding: utf-8 -*-

veclist_ico0 = objvertices("ico.obj", 0)
veclist_ico1 = objvertices("ico.obj", 1)
veclist_dod = objvertices("dod.obj", 0)

def butterflies_task(pos, veclist, axis, speed, color):
	def butterfly_task(vec):
		shot = EntityShot(WORLD, "BUTTERFLY", color)
		shot.Pos = pos
		shot.Velocity = vec * speed
		shot.Upward = axis
		shot.LifeSpan = 75
		
		def rotate(rot = Matrix3.RotationAxis(vec ^ (vec ^ axis), RAD * 2)):
			shot.Velocity *= rot
		shot.AddTask(rotate, 0, shot.LifeSpan, 0)
		
		def shot_child(org = shot):
			for i in range(5):
				shot = EntityShot(WORLD, "BUTTERFLY", color)
				shot.Pos = org.Pos
				shot.Velocity = org.Velocity * (1 + i * 0.5)
				shot.Upward = org.Upward
				shot.LifeSpan = 300
				shot.Spawn()
		shot.AddTask(shot_child, 0, 1, shot.LifeSpan)
		shot.Spawn()
	
	for vec in veclist:
		if abs(vec * axis) > 0.95: continue
		butterfly_task(vec)

def butterflies_to_target_task(vec, axis, color):
	mat = Matrix3.RotationAxis(vec ^ axis, RAD * 7)
	
	for i in range(30):
		shot = EntityShot(WORLD, "BUTTERFLY", color)
		shot.Velocity = vec * 2
		shot.LifeSpan = 300
		
		def turn(shot = shot):
			shot.Velocity = +(TARGET_BONE.WorldPos - shot.Pos) * 8
		shot.AddTask(turn, 0, 1, 60)
		shot.Spawn()
		
		vec *= mat

def task():
	for axis in veclist_dod:
		butterflies_task(Vector3(0, 0, -30), veclist_ico1, axis, 5, 0x0050A0)
		butterflies_task(Vector3(0, 0, -30), veclist_ico1, -axis, 5, 0x0050A0)
		
	for axis in veclist_dod:
		butterflies_task(Vector3(-120, 20, 30), veclist_ico0, axis, 3, 0x006000)
		butterflies_task(Vector3(120, 20, 30), veclist_ico0, -axis, 3, 0x006000)
		
		butterflies_task(Vector3(-240, 0, 30), veclist_ico0, axis, 4, 0xA08000)
		butterflies_task(Vector3(240, 0, 30), veclist_ico0, -axis, 4, 0xA08000)
	
	WORLD.AddTask(lambda t: butterflies_to_target_task(randomvec(), randomvec(), 0x0000A0 if t.ExecutedCount != 3 else 0xA000A0), 25, 4, 150, True)
WORLD.AddTask(task, 270, 3, 0)
