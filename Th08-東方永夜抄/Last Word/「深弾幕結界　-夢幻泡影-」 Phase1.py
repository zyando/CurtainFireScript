# -*- coding: utf-8 -*-

way = 4
angle = RAD * 30

matrices = Matrix3(1, 0, 0, 0, 1, 0, 0, 0, 1), Matrix3(0, 1, 0, 0, 0, 1, 1, 0, 0), Matrix3(0, 0, 1, 1, 0, 0, 0, 1, 0)

vec_axis_list = []
for i in range(way):
	for j in 1, -1:
		vec = Vector3.UnitZ * j * Matrix3.RotationX(angle) * Matrix3.RotationY(RAD * (360.0 / way) * i)
		axis = vec ^ (vec ^ Vector3.UnitY)
		vec *= Matrix3.RotationAxis(axis, RAD * (360.0 / way) * -i)
		
		for mat in matrices[0:3]:
			vec_axis_list.append((vec * mat, axis * mat))

vec_axis_list = [(Vector3.UnitZ, Vector3.UnitY), (-Vector3.UnitZ, Vector3.UnitY)]

curve = CubicBezierCurve(Vector2(0, 0), Vector2(0.9, 0.1), Vector2(0.1, 0.5), Vector2(1, 1))

def task():
	for vec, axis in vec_axis_list:
		spell(
		vec = vec,
		axis = axis,
		prop = ("SCALE", 0xA000A0 if vec.z > 0 else 0x0000A0, 2),
		distance = 512,
		wait_time = 60.0,
		
		get_speed1 = lambda t: 8.0,
		get_speed2 = lambda t: 12.0,
		
		get_vec_rot = lambda t, axis = axis, begin = 0.0, end = 18: Quaternion.RotationAxis(axis, RAD * (begin + (end - begin) * curve.SolveYFromX(t))),
		init_pos = RAD * 0, interval_pos = RAD * 3.65,
		
		num_shot = 6, interval_shot = 2,
		num_task = 16, interval_task = 16,
		
		#停止するフレームを返す関数、引数は最初の弾を0、最後の弾を1とした場合の浮動小数点
		#実際の停止するフレームは、中心に到達するまでに経過するフレーム * pause_frame_func(t)で求められる
		get_pause_frame = lambda t: 0.1 + t * 1.3,
		#再発進するフレームを返す関数、引数は最初の弾を0、最後の弾を1とした場合の浮動小数点
		get_restart_frame = lambda t: 320 * (1 - t * 0.55),
		)
WORLD.AddTask(task, 0, 1, 0)
