# -*- coding: utf-8 -*-

veclist = objvertices("ico.obj", 2)

shot_list = []

test = "test"

def shot_dia_group_task():
	def shot_dia_group(vec, axis, way, distance, speed, color1, color2):
		axis = vec ^ (vec ^ axis)
		velocity = vec * Matrix3.RotationAxis(axis, RAD * -90)
		mat = Matrix3.RotationAxis(axis, RAD * (180.0 / (way - 1)))
		replace_func_list = []

		for i in range(way):
			shot = EntityShot(WORLD, "DIA_BRIGHT", color1)
			shot.Pos = CENTER_BONE.WorldPos + vec * distance
			shot.Velocity = velocity * speed
			shot.SetMotionInterpolationCurve(Vector2(0.3, 0.7), Vector2(0.3, 0.7), 30)

			def pause(shot = shot): shot.Velocity *= 0
			shot.AddTask(pause, 0, 1, 30)
			shot.Spawn()

			def replace(orgn_shot = shot, mat = Matrix3.RotationAxis(axis, RAD * (i % 2 * 2 - 1) * 30)):
				shot = EntityShot(WORLD, "DIA", color2)
				shot.Pos = orgn_shot.Pos
				shot.LookAtVec = -orgn_shot.LookAtVec
				shot.Spawn()

				shot_list.append(shot)

				orgn_shot.Remove()

				def move():
					shot.AddRootBoneKeyFrame()
					shot.Velocity = shot.LookAtVec * mat * 2
				return move
			replace_func_list.append(replace)
			velocity = velocity * mat
		return replace_func_list

	axislist = Vector3.UnitX, Vector3.UnitY, Vector3.UnitZ
	replace_func_list1 = [shot_dia_group(vec, axis, 16, 100, 8, 0x000040, 0xA00000) for vec in veclist for axis in axislist[::-1] if abs(vec * axis) < 0.95]
	replace_func_list2 = [shot_dia_group(vec, axis, 16, 150, 10, 0x400000, 0x0000A0) for vec in veclist[::-1] for axis in axislist if abs(vec * axis) < 0.95]

	def extend_lists(lists):
		x = []
		for l in lists: x.extend(l)
		return x

	num_shot_each_group = 12

	ziped_replace_func_list = [list1 + list2 for list1, list2 in zip(replace_func_list1, replace_func_list2)]
	replace_func_list = [extend_lists(lists) for lists in zip(*[iter(ziped_replace_func_list)] * num_shot_each_group)]

	if len(ziped_replace_func_list) % num_shot_each_group != 0:
		replace_func_list.extend(ziped_replace_func_list[-len(ziped_replace_func_list) % num_shot_each_group:])

	move_func_list = []

	def replace_shot():
		move_func_list.extend([func() for func in replace_func_list.pop()])
	WORLD.AddTask(replace_shot, 0, len(replace_func_list), 60)

	WORLD.AddTask(lambda: [move() for move in move_func_list], 0, 1,  len(replace_func_list) + 80)
WORLD.AddTask(shot_dia_group_task, 480, 2, 0)

if 'REMOVE_FRAME' in globals():
	def remove_shot(num = 512):
		count = 0

		while count < num:
			if len(shot_list) == 0: return True

			orgn = shot_list.pop()

			if orgn.IsRemoved: continue

			orgn.Remove()

			count += 1
	WORLD.AddTask(remove_shot, 0, 0, REMOVE_FRAME - WORLD.FrameCount)
