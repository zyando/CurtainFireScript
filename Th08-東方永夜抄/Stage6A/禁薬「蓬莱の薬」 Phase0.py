# -*- coding: utf-8 -*-

vertices, lines = objlines("hourai_laser.obj")

connected_vtx_dict = {v : [(v2 if v1 == v else v1) for v1, v2 in lines if v1 == v or v2 == v] for v in vertices}

interval = 8

def shot_laser(mat):
	ignore_pos_lines = []
	struct_scale = 160

	def shot_next_laser(pos):
		if pos not in connected_vtx_dict: return

		next_poses = [next_pos for next_pos in connected_vtx_dict[pos] if (next_pos, pos) not in ignore_pos_lines]

		for next_pos in next_poses:
			ignore_pos_lines.append((pos, next_pos))

			vec = (next_pos - pos) * struct_scale
			distance = vec.Length()

			laser = EntityShot(WORLD, "LASER_LINE", 0x0000A0, Vector3(8, 8, distance))
			laser.Pos = CENTER_BONE.WorldPos + pos * mat * struct_scale
			laser.LookAtVec = normalize(vec) * mat
			laser.LifeSpan = interval * 2
			
			morph = laser.CreateVertexMorph(0, lambda v: Vector3(0, 0, -v.z))
			laser.AddMorphKeyFrame(morph, 0, -1)
			laser.AddMorphKeyFrame(morph, 1, 0)
			laser.AddMorphKeyFrame(morph, 0, interval)
			
			morph = laser.CreateVertexMorph(1, lambda v: Vector3(-v.x, -v.y, 0))
			laser.AddMorphKeyFrame(morph, 1, -1)
			laser.AddMorphKeyFrame(morph, 0, 0)
			laser.AddMorphKeyFrame(morph, 0, interval)
			laser.AddMorphKeyFrame(morph, 1, interval * 2)
			
			laser.AddTask(lambda next_pos = next_pos: shot_next_laser(next_pos), 0, 1, interval)
			laser.Spawn()
	shot_next_laser(Vector3(0, 0, 0))
way = 6
matlist = [Matrix3.RotationAxis(Vector3.UnitX, RAD * 180.0 / way * i) for i in range(way)]
WORLD.AddTask(lambda: [shot_laser(mat) for mat in matlist], interval * 6, 0, 0)
