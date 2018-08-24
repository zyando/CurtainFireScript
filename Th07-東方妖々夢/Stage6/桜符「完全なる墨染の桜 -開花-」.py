# -*- coding: utf-8 -*-

veclist = objvertices("ico.obj", 3)

def shot_l():
	for vec in veclist:
		shot = EntityShot(WORLD, "L", 0xA000F0)
		shot.Pos = CENTER_BONE.WorldPos
		shot.Velocity = vec * 5
		shot.LifeSpan = 500
		
		def divide(org = shot):
			for i in range(5):
				shot = EntityShot(WORLD, "L", 0xA000F0)
				shot.Pos = org.Pos
				shot.Velocity = org.Velocity * (6 - i)
				shot.LifeSpan = i * 60
				shot.Spawn()
		shot.AddTask(divide, 0, 1, 45)
		shot.Spawn()
WORLD.AddTask(shot_l, 360, 0, 0)

def shot_dia():
	pos = Vector3(uniform(-500, 500), uniform(-500, 500), gauss() * 400)
	
	for i in 1, -1:
		shot = EntityShot(WORLD, "DIA", 0xA000A0)
		shot.Pos = pos
		shot.Velocity = Vector3.UnitZ * i * uniform(4, 6)
		shot.LifeSpan = 300
		shot.Spawn()
WORLD.AddTask(lambda: [shot_dia() for i in range(6)], 0, 0, 210)

def shot_butterfly(vec, color, homing):
	for i in range(7):
		shot = EntityShot(WORLD, "BUTTERFLY", color)
		shot.Pos = CENTER_BONE.WorldPos
		shot.Velocity = vec * (i + 0.5)
		shot.Upward = Vector3.UnitZ * CENTER_BONE.WorldRot
		shot.LifeSpan = 40
		
		shot.SetMotionInterpolationCurve(Vector2(0.3, 0.7), Vector2(0.3, 0.7), shot.LifeSpan)
		
		def shot_child(org = shot):
			axis = +(vec ^ (vec ^ Vector3.UnitZ * CENTER_BONE.WorldRot))
			
			axis_bone = EntityShot(WORLD, "BONE", 0)
			axis_bone.GetRecordedRot = lambda e: e.Rot
			axis_bone.Pos = org.Pos
			axis_bone.Rot = Matrix3.LookAt(axis, vec)
			
			def rotate(rot = Quaternion.RotationAxis(axis, RAD * 90)): axis_bone.Rot *= rot
			axis_bone.AddTask(rotate, 40, 8, 0)
			
			axis_bone()
			
			for i in range(3):
				shot = EntityShot(WORLD, "BUTTERFLY", color, axis_bone)
				shot.Velocity = Vector3.UnitZ * Matrix3.RotationX(RAD * 30) * Matrix3.RotationZ(RAD * i * 120) * 0.4
				shot.Upward = Vector3.UnitZ
				shot.LifeSpan = 45
				
				def divide(org = shot):
					velocity = +((TARGET_BONE.WorldPos - org.Pos) if False else (org.Velocity * axis_bone.WorldRot))
					
					for i in range(4):
						shot = EntityShot(WORLD, "BUTTERFLY", color)
						shot.Pos = org.WorldPos
						shot.Velocity = velocity * (1.5 + i)
						shot.Upward = axis
						shot.LifeSpan = (5 - i) * 100
						shot.Spawn()
				shot.AddTask(divide, 0, 1, shot.LifeSpan)
				shot.Spawn()
		shot.AddTask(shot_child, 0, 1, shot.LifeSpan)
		shot.Spawn()

way = 5
def task(color, veclist = [Vector3.UnitZ * Matrix3.RotationY(RAD * 60) * Matrix3.RotationZ(RAD * 360.0 / way * i) for i in range(way)]):
	mat = Matrix3.RotationZ(math.pi * 2 * random())
	
	for i, vec in enumerate(veclist):
		shot_butterfly(vec * mat, color, i % 2)
WORLD.AddTask(lambda: task(0x00A0A0), 150, 4, 150)
WORLD.AddTask(lambda: task(0xA000A0), 150, 4, 180)
