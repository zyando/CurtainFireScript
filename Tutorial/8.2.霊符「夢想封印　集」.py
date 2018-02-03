# -*- coding: utf-8 -*-
from random import random, randint

#白の札弾を扇状に発射するタスクを追加

veclist = []
objvertices("ico.obj", lambda v: veclist.append(+v), 1)

def shot_m():
	for vec in veclist:
		shot = EntityShot(WORLD, "M", 0xFFFFFF)
		shot.Velocity = vec * 2
		shot.LivingLimit = 200
		shot()
WORLD.AddTask(shot_m, 30, 10, 10)

def task1(number_of_way = 8):
	#最初に扇状のベクトルのリストを作成する
	#始点となるベクトルを少しずつ回転させて扇状にする
	
	#randomvec()はランダムな単位ベクトルを生成する関数。デフォルトでインポートされている
	#始点となるベクトル
	vec = randomvec()
	
	#回転軸。^はベクトルの外積の演算子
	#v1 ^ (v1 ^ v2) と書くとv2と交わるv1に垂直なベクトルを得られる（これ頻繁に使う）
	axis = vec ^ (vec ^ randomvec())
	#randomは2行目でインポートした関数。0~1のランダムな少数を生成する
	#回転行列。axisを軸として回転する
	mat = Matrix3.RotationAxis(axis, RAD * (20 + random() * 20))
	
	#ベクトルのリスト
	amulet_veclist = []
	#回転させながらamulet_veclistに追加する
	for i in range(number_of_way):
		amulet_veclist.append(vec)
		#ベクトルを回転させる
		vec = vec * mat
	
	#下で定義したshot_amuletを実行する関数
	def task2():
		shot_amulet(amulet_veclist.pop())
	#WORLDにタスクを追加。
	#間隔はrandint(1, 5)で1~5のランダムな整数を生成して指定している
	WORLD.AddTask(task2, randint(1, 5), number_of_way, 0)
WORLD.AddTask(task1, 90, 5, 10)

#札弾を発射する関数。
#第一引数は発射するベクトル
def shot_amulet(vec):
	#速度を変えながら16個の弾を発射する
	for i in range(16):
		#白の札弾を生成
		shot = EntityShot(WORLD, "AMULET", 0xFFFFFF)
		#移動量を設定
		shot.Velocity = vec * (0.5 * i + 2)
		#補間曲線を適用
		shot.SetMotionInterpolationCurve(Vector2(0.3, 0.7), Vector2(0.3, 0.7), 40)
		#寿命を設定
		shot.LivingLimit = 40
		shot()