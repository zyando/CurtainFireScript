# -*- coding: utf-8 -*-

#全方位に弾を発射するスクリプト

veclist = []
objvertices("ico.obj", lambda v: veclist.append(v))

for vec in veclist:
	shot = EntityShot(WORLD, "S", 0xFF0000)
	
	shot.Velocity = vec * 2
	
	#モーション補間曲線を適用する。
	#第一、二引数は制御点の座標の二次元ベクトル、第三引数は補間曲線を適用するフレーム数
	shot.SetMotionInterpolationCurve(Vector2(0.1, 0.9), Vector2(0.9, 0.1), 60)
	
	shot()