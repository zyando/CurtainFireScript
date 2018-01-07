# -*- coding: utf-8 -*-

#全方位に弾を発射するスクリプト

#ベクトルを格納するリスト
veclist = []
#objvertices関数でobjファイルの頂点を取得する
#第一引数はResource/Wavefrontフォルダからの相対パス、第二引数は頂点ベクトルを受け取る関数
objvertices("ico.obj", lambda v: veclist.append(v))

for vec in veclist:
	shot = EntityShot(WORLD, "S", 0xFF0000)
	
	shot.Velocity = vec * 2
	
	shot()