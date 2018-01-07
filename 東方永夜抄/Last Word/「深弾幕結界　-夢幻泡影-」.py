# -*- coding: utf-8 -*-

distance_circle = 1024.0

def task(veclist, axislist, propfunc, speed1, speed2, rot_vec, angle_vec, rot_pos, angle_pos, int_shot, num_shot, int_task, num_task, pause_frame_func, restart_frame_func, restart_frame):
	total_num = num_shot * num_task
	total_num_mult = 1.0 / total_num
	
	frame_num = distance_circle / speed1
	
	for vec in veclist:
		for axis in axislist:
			if abs(vec * axis) > 0.99: 
				continue
			prop = propfunc(vec, axis)
			axis = vec ^ (vec ^ axis)
			
			parent = EntityShot(WORLD, "BONE", 0xFFFFFF)
			parent.Recording = Recording.LocalMat
			parent.Pos = TARGET_BONE.WorldPos
			parent.Rot = Quaternion.RotationAxis(axis, rot_pos)
			parent()
			
			circle = EntityShot(WORLD, "MAGIC_CIRCLE", 0xFFFFFF, parent)
			circle.Recording = Recording.LocalMat
			circle.Pos = vec * distance_circle
			circle.Rot = Matrix3.LookAt(vec, Vector3.UnitY)
			
			for vert in circle.ModelData.Vertices:
				vert.Pos = vert.Pos * 3
			circle()
			
			entity = Entity(WORLD)
			entity.Rot = Quaternion.RotationAxis(axis, rot_vec)
			entity()
			
			rotate_pos = Quaternion.RotationAxis(axis, angle_pos)
			rotate_vec = Quaternion.RotationAxis(axis, angle_vec)
			
			def add_shot_task(task1, axis = axis, entity = entity, circle = circle, prop = prop, rotate_pos = rotate_pos, rotate_vec = rotate_vec):
				def shot_amulet(task2):
					count = (task1.RunCount - 1) * num_shot + task2.RunCount - 1
					
					shot = EntityShot(WORLD, prop)
					shot.Pos = circle.WorldPos
					shot.Velocity = +circle.WorldPos * entity.Rot * -speed1
					shot.Upward = axis
					shot.DiedDecision = lambda e: (e.Pos - parent.Pos).Length > 1024 
					def pause():
						shot.Velocity *= 0
					shot.AddTask(pause, 0, 1, int(frame_num * pause_frame_func(count * total_num_mult)))
					
					def restart(vec = +shot.Velocity):
						shot.Velocity = vec * speed2
					shot.AddTask(restart, 0, 1, int(restart_frame * restart_frame_func(count * total_num_mult)))
					
					shot()
				entity.AddTask(shot_amulet, int_shot, num_shot, 0, True)
			entity.AddTask(add_shot_task, int_task, num_task, 0, True)
			
			def rotate(entity = entity, circle = circle, parent = parent, prop = prop, rotate_pos = rotate_pos, rotate_vec = rotate_vec):
				parent.Rot = parent.Rot * rotate_pos
				entity.Rot = +entity.Rot * rotate_vec
			entity.AddTask(rotate, int_shot, WORLD.MaxFrame / int_shot, 1)
			
			def shot_amulet_outside(circle = circle, prop = prop):
				shot = EntityShot(WORLD, prop)
				shot.Pos = circle.WorldPos
				shot.Velocity = +circle.WorldPos * 2.0
				shot.Upward = axis
				shot.DiedDecision = lambda e: (e.Pos - parent.Pos).Length > 1024
				shot()
			circle.AddTask(shot_amulet_outside, 1, int(num_task * int_task * 0.5), 0)
veclist = []
objvertices("ico.obj", lambda v: veclist.append(+v), 1)

WORLD.AddTask(lambda: task(
veclist,
axislist = [Vector3.UnitX, Vector3.UnitZ],
propfunc = lambda v, a: ShotProperty(AMULET, 0xA00000 if a.x > 0.99 else 0x0000A0),
speed1 = 8.0,
speed2 = 12.0,
rot_vec = RAD * -10,
angle_vec = RAD * 0.1,
rot_pos = RAD * 0.0,
angle_pos = RAD * 1.5,
int_shot = 1,
num_shot = 50,
int_task = 110,
num_task = 2,
#停止するフレームを返す関数、引数は最初の弾を0、最後の弾を1とした場合の浮動小数点
#実際の停止するフレームは、中心に到達するまでに経過するフレーム * pause_frame_func(t)で求められる
pause_frame_func = lambda t: 0.2 + t * 1.2,
#再発進するフレームを返す関数、引数は最初の弾を0、最後の弾を1とした場合の浮動小数点
#実際の停止するフレームは、restart_frame * restart_frame_func(t)で求められる
restart_frame_func = lambda t: 1 - t * 0.4,
restart_frame = 320
), 0, 1, 0)
