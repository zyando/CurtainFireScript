# -*- coding: utf-8 -*-

#上方向に1つ弾を発射するスクリプト

#弾を生成する。第一引数は固定でWORLD、第二引数は弾の種類、第三引数は色をRGBで指定する
shot = EntityShot(WORLD, "S", 0xFF0000)

#1フレームあたりの移動量を三次元ベクトルで指定する
shot.Velocity = Vector3(0, 1, 0)

#弾を配置する
shot()