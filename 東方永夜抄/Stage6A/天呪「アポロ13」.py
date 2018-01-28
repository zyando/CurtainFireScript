# -*- coding: utf-8 -*-

veclist = []
objvertices("ico.obj", lambda v: veclist.append(+v), 2)

def shot_dia_group_task(way = 12):
	def shot_dia_group(vec, axis, angle, fan_angle, distance, speed, color):
		axis = vec ^ (vec ^ axis)
		velocity = vec * Matrix3.RotationAxis(axis, angle)
		mat = Matrix3.RotationAxis(axis, fan_angle / (way + 1))
		shotlist = []
		
		for i in range(way):
			shot = EntityShot(WORLD, "DIA", color)
			shot.Pos = vec * distance
			shot.Velocity = velocity * speed
			shot.SetMotionInterpolationCurve(Vector2(0.3, 0.7), Vector2(0.3, 0.7), 30)
			
			def pause(shot = shot): shot.Velocity *= 0
			shot.AddTask(pause, 0, 1, 30)
			
			shot.ModelData.Materials[0].Shininess = 130
			shot()
			shotlist.append(shot)
			
			velocity = velocity * mat
		return shotlist
	
	shotgroup_list1 = [[shot_dia_group(vec, axis, RAD * -75, RAD * 180, 200, 6, 0x000040) for axis in Vector3.UnitX, Vector3.UnitZ if abs(vec * axis) < 0.95] for vec in veclist]
	shotgroup_list2 = [[shot_dia_group(vec, axis, RAD * 10, RAD * 90, 300, 8, 0x400000) for axis in Vector3.UnitZ, Vector3.UnitX if abs(vec * axis) < 0.95] for vec in veclist[::-1]]
	
	def extend_lists(lists):
		x = []
		for l in lists: x.extend(l)
		return x
	
	ziped_shotgroup_list = [list1 + list2 for list1, list2 in zip(shotgroup_list1, shotgroup_list2)]
	shotgroup_list = [extend_lists(lists) for lists in zip(*[iter(ziped_shotgroup_list)]*4)]
	
	if len(ziped_shotgroup_list) % 4 != 0:
		shotgroup_list.append(extend_lists(ziped_shotgroup_list[1 - len(ziped_shotgroup_list) % 4:]))
	
	replaced_shotlist = []
	
	def replace_shot(task):
		for i in range(task.RunCount):
			if i >= len(shotgroup_list) or len(shotgroup_list[i][0]) == 0: continue
			
			for shotgroup in shotgroup_list[i]:
				old = shotgroup.pop()
				
				shot = EntityShot(WORLD, "DIA", 0xA00000 if old.Property.Color == 0x000040 else 0x0000A0)
				shot.Pos = old.Pos
				shot.LookAtVec = -old.LookAtVec
				
				shot()
				replaced_shotlist.append(shot)
				
				old.OnDeath()
	WORLD.AddTask(replace_shot, 0, len(shotgroup_list) + way + 1, 60, True)
	
	def move():
		for shot in replaced_shotlist:
			shot.LivingLimit = shot.FrameCount + 600
			shot.Velocity = shot.LookAtVec * 3.0
	WORLD.AddTask(move, 0, 1,  len(shotgroup_list) + way + 80)
WORLD.AddTask(shot_dia_group_task, 480, 2, 10)