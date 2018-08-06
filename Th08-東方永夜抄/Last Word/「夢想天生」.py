# -*- coding: utf-8 -*-

veclist = []
num_way = 8
mat = Matrix3.RotationAxis(Vector3.UnitY, RAD * (360 / num_way))
vec = Vector3.UnitZ

for i in range(num_way):
	veclist.append(vec)
	vec  = vec * mat

def world_task(axis, r):
	root = EntityShot(WORLD, "BONE", 0xFFFFFF)
	root.GetRecordedRot = lambda e: e.Rot
	root.Pos = CENTER_BONE.WorldPos
	root.Rot = Quaternion.RotationAxis(Vector3.UnitY ^ axis, math.acos(Vector3.UnitY * axis))
	
	def follow(rotate = Quaternion.RotationAxis(Vector3.UnitY, RAD * 8)):
		root.Rot = rotate * root.Rot
	root.AddTask(follow, 0, 470, 0)
	root()
	
	def create_shot_m(vec):
		shot = EntityShot(WORLD, "M_ICO", 0xFFFFFF, root)
		shot.Pos = vec * r
		shot()
		return shot
	shotlist = [create_shot_m(v) for v in veclist]
	
	def shot_task_func1(task):
		flag = task.ExecutedCount == 0
		
		upward = Vector3.UnitY * root.WorldMat
		mat = Matrix3.RotationAxis(upward, RAD * uniform(0, 40))
		
		shotStack = list(shotlist)
		def shot_task_func2():
			parentShot = shotStack.pop()
			vec = +(parentShot.WorldPos - root.WorldPos) * mat
			shot_amulet(parentShot.WorldPos, vec, upward)
		root.AddTask(shot_task_func2, 1 if flag else randint(3, 6), len(shotStack), 0)
		task.ExecutingInterval -= 10
	root.AddTask(shot_task_func1, 90, 4, 10, True)
world_task(+Vector3(1, 1, -0.5), 100.0)
world_task(+Vector3(1, -1, 0.5), 140.0)

def shot_amulet(pos, vec, upward):
	def shot_func1(original):
		shot = EntityShot(WORLD, "AMULET", 0xFF00FF)
		shot.Pos = original.Pos
		shot.Velocity = +(TARGET_BONE.WorldPos - shot.Pos) * 24.0
		shot.Upward = original.Upward
		shot.LifeSpan = 100
		
		shot()
	
	def shot_func2(original):
		shot = EntityShot(WORLD, "S", 0xFF00FF)
		shot.Pos = original.Pos
		shot.Upward = original.Upward
		shot.AddTask(lambda s = shot :shot_func1(s) , 0, 1, 10)
		shot.LifeSpan = 10
		
		shot()
	
	def shot_func3(original):
		shot = EntityShot(WORLD, "AMULET", 0xFF0000)
		shot.Pos = original.Pos
		shot.Velocity = (TARGET_BONE.WorldPos - shot.Pos) * 0.0025
		shot.Upward = original.Upward
		shot.SetMotionInterpolationCurve(Vector2(0.2, 0.8), Vector2(0.2, 0.8), 40)
		shot.AddTask(lambda s = shot :shot_func2(s) , 0, 1, 40)
		shot.LifeSpan = 40
		
		shot()
	
	def shot_func4(original):
		shot = EntityShot(WORLD, "S", 0xFF0000)
		shot.Pos = original.Pos
		shot.Upward = original.Upward
		shot.AddTask(lambda s = shot :shot_func3(s) , 0, 1, 10)
		shot.LifeSpan = 10
		shot()
	
	for j in range(24):
		shot = EntityShot(WORLD, "AMULET", 0xFFFFFF)
		shot.Pos = pos
		shot.Velocity = vec * (1 * j + 4)
		shot.Upward = upward
		shot.AddTask(lambda s = shot: shot_func4(s) , 0, 1, 30)
		shot.SetMotionInterpolationCurve(Vector2(0.2, 0.8), Vector2(0.2, 0.8), 30)
		shot.LifeSpan = 30
		shot()
