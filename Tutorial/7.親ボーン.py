# -*- coding: utf-8 -*-

#回りながら移動する弾を発射する

#ベクトルを格納するリスト
veclist = []

number_of_way = 8
vec = Vector3.UnitY
mat = Matrix3.RotationAxis(Vector3.UnitZ, RAD * 360.0 / number_of_way)

for i in range(number_of_way):
	veclist.append(vec)
	vec = vec * mat

parent = EntityShot(WORLD, "BONE", 0xFFFFFF)
parent.GetRecordedRot = lambda e: e.Rot
parent.Velocity = Vector3.UnitZ * 3

def rotate(rot = Quaternion.RotationAxis(Vector3.UnitZ, RAD * 90)):
	parent.Rot *= rot
parent.AddTask(rotate, 15, 0, 0)

parent()

for vec in veclist:
	shot = EntityShot(WORLD, "S", 0xFF0000, parent)
	
	shot.Velocity = vec
	
	shot()