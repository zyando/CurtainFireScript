# -*- coding: utf-8 -*-

cube_edges = []

border_range = 800 * 800

def get_time_to_vanish(pos, velocity):
	if WORLD.FrameCount > BORDER_BOMB_FRAME + BORDER_BOMB_ACTIVETIME: return 1E+5
	
	pos += velocity * (BORDER_BOMB_FRAME - WORLD.FrameCount)
	vec = pos - YUKARI_HAND_BONE.WorldPos
	
	distance = vec * vec
	
	return BORDER_BOMB_FRAME - WORLD.FrameCount + (distance / border_range) * 30 + randint(0, 10)

for vtx in [Vector3(xz * y, y, xz) for xz in [1, -1] for y in [1, -1]]:
	for mat in Matrix3(-1, 1, 1), Matrix3(1, -1, 1), Matrix3(1, 1, -1):
		cube_edges.append((vtx, vtx * mat))

def task(color, scale):
	border = EntityShot(WORLD, "CUBE_BORDER", color, scale)
	border.Pos = YUKARI_HAND_BONE.WorldPos
	
	border.GetRecordedRot = lambda e: e.Rot
	border.LivingLimit = BORDER_BOMB_ACTIVETIME + 15

	morph = border.CreateVertexMorph(0, lambda v: -v * 0.99)
	border.AddMorphKeyFrame(morph, 1, 0)
	border.AddMorphKeyFrame(morph, 0, 15)
	border.AddMorphKeyFrame(morph, 0, border.LivingLimit - 15)
	border.AddMorphKeyFrame(morph, 1, border.LivingLimit)

	def rotate(rot = Quaternion.RotationAxis(randomvec(), RAD * 90)): border.Rot *= rot
	WORLD.AddTask(rotate, 30, 0, 0)

	def effect():
		for i in range(16):
			shot = EntityShot(WORLD, "DIA", color, Vector3(1, 1, 10))
			shot.Velocity = randomvec() * 80
			shot.Pos = YUKARI_HAND_BONE.WorldPos + +shot.Velocity * scale * uniform(0.1, 1)
			shot.LivingLimit = 50
			shot()
	WORLD.AddTask(effect, 0, border.LivingLimit ,0)
	border()

def quadruple_barrier():
	task(0xFF00FF, 480)
	task(0xFF0000, 440)
	task(0x0000FF, 400)
	task(0xA000A0, 360)
WORLD.AddTask(quadruple_barrier, 0, 1, BORDER_BOMB_FRAME)
