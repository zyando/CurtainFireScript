# -*- coding: utf-8 -*-

veclist, linelist = objlines("rose_lowpolygon1.obj")

def shot_rose(rose_pos, rose_rot, shot_factory, blooming_frame, init_scale = Matrix3(0.2, 0.4, 0.2), scale = 1.6):
	vertlist = [v for line in linelist for v in line]
	edges = [v for v in veclist if vertlist.count(v) == 1]
	poslist = []
	
	def task(pos):
		poslist.append(pos)
		
		next_poslist = [[p for p in line if (p != pos)][0] for line in linelist if (pos in line and line[0] != line[1])]
		
		shot = shot_factory()
		shot.Pos = rose_pos + pos * rose_rot * scale * init_scale
		shot.LifeSpan = 900
		shot()
		
		def move():
			shot.Velocity = (pos * rose_rot * scale - pos * rose_rot * scale * init_scale) * (1.0 / 8)
			shot.SetMotionInterpolationCurve(Vector2(0.2, 0.8), Vector2(0.2, 0.8), 8)
		shot.AddTask(move, 0, 1, blooming_frame - WORLD.FrameCount)
		
		def stop():
			shot.Velocity *= 0
		shot.AddTask(stop, 0, 1, blooming_frame + 8 - WORLD.FrameCount)
		
		def next_task():
			for next_pos in next_poslist:
				if next_pos not in poslist:
					task(next_pos)
		shot.AddTask(next_task, 0, 1, 1)
		shot()
	
	for v in edges:
		task(v)

def stalk(pos, vec, color):
	entity = EntityMoving(WORLD)
	entity.Pos = pos
	entity.Velocity = vec * 4
	entity()
	
	def turn():
		entity.Velocity *= Matrix3.RotationAxis(randomvec(), RAD * 30)
	WORLD.AddTask(turn, lambda i: randint(30, 60), 20, 40)
	
	def shot_stalk():
		shot = EntityShot(WORLD, "M", 0x004000)
		shot.Pos = entity.Pos
		shot.LifeSpan = 900
		shot()
	WORLD.AddTask(shot_stalk, 5, 200, 0)
	
	def blooming():
		shot_rose(entity.Pos, Matrix3.RotationAxis(randomvec(), RAD * random() * 180), lambda: EntityShot(WORLD, "S", color), 240)
	WORLD.AddTask(blooming, lambda i: randint(40, 80), 2, randint(10, 60))

for vec in objvertices("ico.obj", 0):
	stalk(vec * 400, vec * Matrix3.RotationAxis(vec ^ (vec ^ Vector3.UnitY), RAD * 90), 0xA00000 if uniform(-1, 1) > 0 else 0x0000A0)
