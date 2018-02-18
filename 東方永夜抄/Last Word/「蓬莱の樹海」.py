# -*- coding: utf-8 -*-

colorlist = [0xA00000, 0x00A000, 0x0000A0, 0xA0A000, 0xA000A0, 0x00A0A0, 0xFF20A0]

way = 6
mat = Matrix3.RotationAxis(Vector3.UnitZ, RAD * (360 / way))
vec = Vector3.UnitY

veclist = [Vector3.Zero]

for i in range(way):
	veclist.append(vec)
	vec = vec * mat

root = EntityShot(WORLD, "BONE", 0xFFFFFF)
root.Recording = Recording.LocalMat
root.Pos = Vector3(0, 0, 160)

rot1 = Quaternion.RotationAxis(Vector3.UnitZ, RAD * 5)
rot2 = Quaternion.RotationAxis(randomvec(), RAD * 5)
def rotate():
	root.Rot = rot1 * root.Rot
	root.Rot = root.Rot * rot2
root.AddTask(rotate, 3, 120, 0)
root()

colorstack = list(colorlist)

def died_decision1(entity):
	if abs(entity.Pos.x) > 400 or abs(entity.Pos.y) > 400 or entity.Pos.z > 800 or entity.Pos.z < -300:
		shot = EntityShot(WORLD, "DIA", 0xFFFFFF)
		shot.Pos = entity.Pos
		shot.Velocity = -entity.Velocity
		shot.DiedDecision = died_decision2
		shot()
		return True
	return False

died_decision2 = lambda e: (abs(e.Pos.x) > 400 or abs(e.Pos.y) > 400 or e.Pos.z > 800 or e.Pos.z < -300) and e.FrameCount > 10

for vec in veclist:
	color = colorstack.pop()
	
	parent = EntityShot(WORLD, "MAGIC_CIRCLE", 0xA0A0A0, root)
	parent.Recording = Recording.LocalMat
	parent.Pos = OWNER_BONE.WorldPos + vec * 20
	
	def shot_dia(parent = parent, color = color):
		vec = Vector3.UnitX * parent.WorldMat
		
		for i in range(2):
			shot = EntityShot(WORLD, "DIA", color)
			shot.Pos = parent.WorldPos
			shot.Velocity = vec * 2.4
			shot.DiedDecision  = died_decision1
			shot()
			
			vec = -vec
	parent.AddTask(shot_dia, 3, 120, 0)
	parent()
veclist = objvertices("ico.obj", 0)

for vec in veclist:
	for axis in [Vector3.UnitX, Vector3.UnitZ]:
		parent = Entity(WORLD)
		parent.Pos = vec
		
		def shot_s(task, parent = parent, mat = Matrix3.RotationAxis(axis, RAD * 10)):
			parent.Pos = parent.Pos * mat
			
			shot = EntityShot(WORLD, "S", colorlist[task.ExecutedCount % len(colorlist)])
			shot.Pos = OWNER_BONE.WorldPos
			shot.Velocity = parent.Pos * 3.4
			shot.LivingLimit = 160
			shot()
		parent.AddTask(shot_s, 10, 40, 0, True)
		parent()
		
