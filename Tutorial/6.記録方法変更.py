# -*- coding: utf-8 -*-

#回転する魔法陣を配置するスクリプト

shot = EntityShot(WORLD, "MAGIC_CIRCLE", 0xFFFFFF)

#通常ではVelocityが変更された時にキーフレームを登録するが、
#RecordingをLocalMatに変更することでPosまたはRotが変更された時にキーフレームを登録することができる
shot.Recording = Recording.LocalMat

#回転させる関数を定義する。Quaternion.RotationAxisの第一引数は回転軸、第二引数は回転角度をラジアンで指定する
#RADは math.pi / 180.0 の定数
def rotate(rot = Quaternion.RotationAxis(Vector3.UnitZ, RAD * 90)):
	shot.Rot *= rot
shot.AddTask(rotate, 30, 0, 0)

shot()