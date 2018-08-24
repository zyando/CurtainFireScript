# -*- coding: utf-8 -*-

COLORS = (0xE60012, 0x600000), (0xF39800, 0x702000), (0xFFF100, 0x606000), (0x009944, 0x005020), (0x0068B7, 0x003070), (0x1D2088, 0x001050), (0x920783, 0x400040)

poslist = [Vector3.UnitZ * 250 - Vector3.UnitZ * 120 * Matrix3.RotationY(RAD * (i - 3) * 12) for i in range(7)]

def get_collide_time(pos, vec, plane = [Vector3(300, 300, 500), Vector3(-300, -300, -200)]):
	min_dis = 1E5
	for i in range(2):
		v = vec[i] if abs(vec[i]) > 0.001 else 0.001 
		
		if v > 0:
			dis = (plane[0][i] - pos[i]) / v
		else:
			dis = (plane[1][i] - pos[i]) / v
		min_dis = min(min_dis, dis)
	return int(min_dis)

def task(pos, color1, color2):
	mgc = EntityShot(WORLD, "MAGIC_CIRCLE", 0x505050, 2)
	mgc.Pos = pos
	mgc.LookAtVec = +(Vector3.UnitZ * 250 - mgc.Pos)
	
	def shot_dia(vec):
		shot = EntityShotStraight(WORLD, "DIA_BRIGHT", color2)
		shot.Pos = mgc.Pos
		shot.Velocity = vec * 6
		shot.LifeSpan = get_collide_time(shot.Pos, shot.Velocity)
		
		def replace(org = shot):
			shot = EntityShotStraight(WORLD, "DIA", color1)
			shot.Pos = org.Pos
			shot.Velocity = +(TARGET_BONE.WorldPos - org.Pos) * 5
			shot.LifeSpan = 300
			shot.Spawn()
		mgc.AddTask(replace, 0, 1, shot.LifeSpan)
		shot.Spawn()
	
	def init_shot(veclist = objvertices("ico.obj", 3)):
		mat = Matrix3.LookAt(mgc.LookAtVec, Vector3.UnitY)
		for vec in veclist:
			shot_dia(vec * mat)
	mgc.AddTask(init_shot, 0, 1, 0)
	
	def dia_task(task, veclist = [Vector3.UnitX * Matrix3.RotationZ(RAD * 30 * i) for i in [1, -1]]):
		i = (task.ExecutedCount % 2) * 2 - 1
		way = 12
		
		def shot_dia_task(task):
			vec = Vector3.UnitX * Matrix3.RotationZ(RAD * 30 * task.ExecutedCount / float(way) * i)
			
			for j in 1, -1:
				shot_dia(vec * j)
		mgc.AddTask(shot_dia_task, 2, way, 0, True)
	mgc.AddTask(dia_task, 90, 6, 210, True)
	
	mgc()
for idx, pos in enumerate(poslist):
	task(pos, *COLORS[idx])

def shot_rainbow_s(vec, axis):
	binder = [vec]
	
	def shot_s(task, rot = Matrix3.RotationAxis(vec ^ (vec ^ axis), RAD * 15)):
		shot = EntityShotStraight(WORLD, "S", COLORS[task.ExecutedCount % len(COLORS)][0])
		shot.Velocity = binder[0] * 4
		shot.LifeSpan = 240
		shot.Spawn()
		
		if task.ExecutedCount > 10:
			binder[0] *= rot
	WORLD.AddTask(shot_s, 4, 160, 180, True)

for vec in objvertices("ico.obj", 1):
	for axis in Vector3.Units:
		if vec * axis > 0.95: continue
		
		shot_rainbow_s(vec, axis)
