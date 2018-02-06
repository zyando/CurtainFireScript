# -*- coding: utf-8 -*-

#発射された10フレーム後に移動方向を反転する弾を30フレームごとに発射するスクリプト

#objvertices関数でobjファイルの頂点を取得する
veclist = objvertices("ico.obj")

#弾を発射する関数を定義する
def shot():
	for vec in veclist:
		shot = EntityShot(WORLD, "S", 0xFF0000)
		
		shot.Velocity = vec * 2
		
		#弾を反転する関数を定義する。
		#後に代入される可能性のある変数を関数内で参照する場合、デフォルト引数として宣言することで参照を保持する
		def reverse(shot = shot):
			#移動量に-1をかけて反転させる
			shot.Velocity *= -1
		#タスクを追加する。
		#第一引数は実行する関数、第二引数は実行する間隔、第三引数は実行する回数、第四引数は実行するまでの待機時間
		#今回は60フレームに一回だけ実行するので、間隔は0、回数は1を指定している
		shot.AddTask(reverse, 0, 1, 60)
		
		shot()
#WORLDにもAddTask関数を使用できる
WORLD.AddTask(shot, 30, 5, 0)