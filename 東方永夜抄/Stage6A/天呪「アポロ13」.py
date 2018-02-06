# -*- coding: utf-8 -*-

veclist = objvertices("ico.obj", 2)

def shot_dia_group_task():
	def shot_dia_group(vec, axis, way, distance, speed, color1, color2):
		axis = vec ^ (vec ^ axis)
		velocity = vec * Matrix3.RotationAxis(axis, RAD * -90)
		mat = Matrix3.RotationAxis(axis, RAD * (180.0 / (way - 1)))
		replace_func_list = []
		
		for i in range(way):
			shot = EntityShot(WORLD, "DIA", color1)
			shot.Pos = vec * distance
			shot.Velocity = velocity * speed
			shot.SetMotionInterpolationCurve(Vector2(0.3, 0.7), Vector2(0.3, 0.7), 30)
			
			def pause(shot = shot): shot.Velocity *= 0
			shot.AddTask(pause, 0, 1, 30)
			
			shot.ModelData.Materials[0].Shininess = 130
			shot()
			
			def replace(orgn_shot = shot, mat = Matrix3.RotationAxis(axis, RAD * (i % 2 * 2 - 1) * 30)):
				shot = EntityShot(WORLD, "DIA", color2)
				shot.Pos = orgn_shot.Pos
				shot.LookAtVec = -orgn_shot.LookAtVec
				shot()
				
				orgn_shot.OnDeath()
				
				def move():
					shot.AddRootBoneKeyFrame()
					shot.Velocity = shot.LookAtVec * mat * 2
				return move
			replace_func_list.append(replace)
			velocity = velocity * mat
		return replace_func_list
	
	axislist = Vector3.UnitX, Vector3.UnitZ
	replace_func_list1 = [shot_dia_group(vec, axis, 12, 100, 6, 0x000040, 0xA00000) for vec in veclist for axis in axislist[::-1] if abs(vec * axis) < 0.95]
	replace_func_list2 = [shot_dia_group(vec, axis, 12, 150, 8, 0x400000, 0x0000A0) for vec in veclist[::-1] for axis in axislist if abs(vec * axis) < 0.95]
	
	def extend_lists(lists):
		x = []
		for l in lists: x.extend(l)
		return x
	
	ziped_replace_func_list = [list1 + list2 for list1, list2 in zip(replace_func_list1, replace_func_list2)]
	replace_func_list = [extend_lists(lists) for lists in zip(*[iter(ziped_replace_func_list)] * 8)]
	
	if len(ziped_replace_func_list) % 8 != 0:
		replace_func_list.append(ziped_replace_func_list[1 - len(ziped_replace_func_list) % 8:])
	
	move_func_list = []
	
	def replace_shot():
		move_func_list.extend([func() for func in replace_func_list.pop()])
	WORLD.AddTask(replace_shot, 0, len(replace_func_list), 60)
	
	WORLD.AddTask(lambda: [move() for move in move_func_list], 0, 1,  len(replace_func_list) + 80)
WORLD.AddTask(shot_dia_group_task, 480, 1, 10)