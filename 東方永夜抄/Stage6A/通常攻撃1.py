# -*- coding: utf-8 -*-

veclist1 = []
objvertices("ico.obj", lambda v: veclist1.append(+v), 1)

veclist2 = []
objvertices("ico.obj", lambda v: veclist2.append(+v), 2)

def task(task, colors_tuple = ((0x400000, 0xA00000), (0x000040, 0x0000A0))):
	colors = colors_tuple[task.RunCount % 2]
	
	def shot_dia(pos, vec, angle, color1, color2):
		vec += pos
		
		shot = EntityShot(WORLD, "DIA", color1)
		shot.Pos = pos * 100
		shot.Velocity = vec * 3
		shot.SetMotionInterpolationCurve(Vector2(0.3, 0.7), Vector2(0.3, 0.7), 30)
		
		shot.ModelData.Materials[0].Shininess = 130
		
		def pause(): shot.Velocity *= 0
		shot.AddTask(pause, 0, 1, 30)
		
		vec = vec * Matrix3.RotationAxis(vec ^ (vec ^ pos), angle)
		
		def rotate(): shot.LookAtVec = vec
		shot.AddTask(pause, 0, 1, 40)
		shot.AddTask(lambda: shot.AddRootBoneKeyFrame(), 0, 2, 39)
		
		def replace(old_shot = shot):
			old_shot.OnDeath()
			
			shot = EntityShot(WORLD, "DIA", color2)
			shot.Pos = old_shot.Pos
			shot.LookAtVec = -vec
			shot()
			
			def move(): 
				shot.Velocity = vec * -2.0
				shot.LivingLimit = shot.FrameCount + 380
			return move
		shot()
		
		return replace
	
	mat = Matrix3.RotationAxis(randomvec(), RAD * 30)
	
	replace_func_list = [[shot_dia(p * mat, v * mat, RAD * (10 if i % 2 == 0 else -10), *colors) for i, v in enumerate(veclist1) if p * v > -0.6] for p in veclist2]
	def extend_lists(lists):
		x = []
		for l in lists: x.extend(l)
		return x
	ziped_replace_func_list = [extend_lists(lists) for lists in zip(*[iter(replace_func_list)]*4)]
	
	if len(replace_func_list) % 4 != 0:
		ziped_replace_func_list.append(extend_lists(replace_func_list[-(len(replace_func_list) % 4):]))
	
	move_func_list = []
	
	WORLD.AddTask(lambda: move_func_list.extend([f() for f in ziped_replace_func_list.pop()]), 0, len(ziped_replace_func_list), 40)
	WORLD.AddTask(lambda: [f() for f in move_func_list], 0, 1, len(ziped_replace_func_list) + 40)
WORLD.AddTask(task, 240, 5, 0, True)
