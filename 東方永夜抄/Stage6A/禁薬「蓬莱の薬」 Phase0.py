# -*- coding: utf-8 -*-

WORLD.MaxFrame = 7271 - 322

def phase0():
	vertices, lines = objlines("hourai_laser.obj")

	connected_vtx_dict = {v : [(v2 if v1 == v else v1) for v1, v2 in lines if v1 == v or v2 == v] for v in vertices}

	def shot_laser(mat):
		ignore_pos_lines = []
		struct_scale = 80

		def shot_next_laser(pos):
			if pos not in connected_vtx_dict: return

			next_poses = [next_pos for next_pos in connected_vtx_dict[pos] if (next_pos, pos) not in ignore_pos_lines]

			for next_pos in next_poses:
				ignore_pos_lines.append((pos, next_pos))

				vec = (next_pos - pos) * struct_scale
				distance = vec.Length()

				laser = EntityShot(WORLD, "LASER_LINE", 0x0000A0, Vector3(5, 5, distance))
				laser.Pos = pos * mat * struct_scale
				laser.LookAtVec = +vec * mat
				laser.LivingLimit = 20

				morph = laser.CreateVertexMorph(lambda v, scale = Matrix3(-0.9, -0.9, 0): v * scale)
				laser.AddMorphKeyFrame(morph, 1, 0)
				laser.AddMorphKeyFrame(morph, 0, 10)
				laser.AddMorphKeyFrame(morph, 1, 20)

				laser.AddTask(lambda next_pos = next_pos: shot_next_laser(next_pos), 0, 1, 7)
				laser()

				shot = EntityShot(WORLD, "S", 0x0000A0, 2)
				shot.LivingLimit = 7
				shot.Pos = laser.Pos
				shot.Velocity = vec * mat * (1.0 / shot.LivingLimit)
				shot()
		shot_next_laser(Vector3(0, 0, 0))
	way = 6
	matlist = [Matrix3.RotationAxis(Vector3.UnitX, RAD * 180.0 / (way - 1) * i) for i in range(way)]
	WORLD.AddTask(lambda: [shot_laser(mat) for mat in matlist], 42, WORLD.MaxFrame / 42, 0)
WORLD.AddTask(phase0, 0, 1, 0)
