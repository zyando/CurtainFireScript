# -*- coding: utf-8 -*-

#全方位に弾を発射するスクリプト

#ベクトルを格納するリスト
veclist = []
#objvertices関数でobjファイルの頂点を取得する
#第三引数に分割数を指定できる
#+vのように+演算子でベクトルを正規化できる。
objvertices("ico.obj", lambda v: veclist.append(+v), 1)

for vec in veclist:
	shot = EntityShot(WORLD, "S", 0xFF0000)
	
	shot.Velocity = vec * 2
	
	shot()