# -*- coding: utf-8 -*-

#全方位に弾を発射するスクリプト

#objvertices関数でobjファイルの頂点を取得する
#第二引数に分割数を指定できる
veclist = objvertices("ico.obj", 1)

for vec in veclist:
	shot = EntityShot(WORLD, "S", 0xFF0000)
	
	shot.Velocity = vec * 2
	
	shot()