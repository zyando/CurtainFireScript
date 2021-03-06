# -*- coding: utf-8 -*-

way = 3
angle = RAD * 30

matrices = Matrix3(1, 0, 0, 0, 1, 0, 0, 0, 1), Matrix3(0, 1, 0, 0, 0, 1, 1, 0, 0), Matrix3(0, 0, 1, 1, 0, 0, 0, 1, 0)

vec_axis_list = []
for i in range(way):
	for j in 1, -1:
		vec = Vector3.UnitZ * j * Matrix3.RotationX(angle) * Matrix3.RotationY(RAD * (360.0 / way) * i)
		axis = cross2(vec, Vector3.UnitY)
		vec *= Matrix3.RotationAxis(axis, RAD * (360.0 / way) * -i)
		
		for mat in matrices[0:3]:
			vec_axis_list.append((vec * mat, axis * mat))

def task():
	for vec, axis in vec_axis_list:
		for i in [1, 1.1]:
			spell(
			vec = vec,
			axis = axis,
			prop = ("AMULET", 0xA000A0 if vec.z > 0 else 0xA00000),
			distance = 1024,
			wait_time = 60.0,
			
			get_speed1 = lambda t, i = i: 12.0 + t * i * 2,
			get_speed2 = lambda t: 12.0,
			
			get_vec_rot = lambda t, axis = axis, begin = 0, end = 20: Matrix3.RotationAxis(axis, RAD * (begin + (end - begin) * t)),
			init_pos = RAD * 0, interval_pos = RAD * 4,
			
			num_shot = 220, interval_shot = 1,
			num_task = 1, interval_task = 220,
			
			#停止するフレームを返す関数、引数は最初の弾を0、最後の弾を1とした場合の浮動小数点
			#実際の停止するフレームは、中心に到達するまでに経過するフレーム * pause_frame_func(t)で求められる
			get_pause_frame = lambda t: 0.1 + t * 4,
			#再発進するフレームを返す関数、引数は最初の弾を0、最後の弾を1とした場合の浮動小数点
			get_restart_frame = lambda t: 320 * (1 - t * 0.4),
			)
	
	for vec, axis in vec_axis_list:
		spell(
		vec = vec,
		axis = axis * -1,
		prop = ("AMULET", 0x0000A0),
		distance = 900,
		wait_time = 60.0,
		
		get_speed1 = lambda t: 8.0,
		get_speed2 = lambda t: 12.0,
		
		get_vec_rot = lambda t, begin = 0, end = -10: Quaternion.RotationAxis(axis, RAD * (begin + (end - begin) * t)),
		init_pos = RAD * 0, interval_pos = RAD * 4,
		
		num_shot = 3, interval_shot = 1,
		num_task = 21, interval_task = 10,
		
		#停止するフレームを返す関数、引数は最初の弾を0、最後の弾を1とした場合の浮動小数点
		#実際の停止するフレームは、中心に到達するまでに経過するフレーム * pause_frame_func(t)で求められる
		get_pause_frame = lambda t: 0.1 + t * 1.0,
		#再発進するフレームを返す関数、引数は最初の弾を0、最後の弾を1とした場合の浮動小数点
		get_restart_frame = lambda t: 350 * (1 - t * 0.5),
		)
WORLD.AddTask(task, 0, 1, 0)
