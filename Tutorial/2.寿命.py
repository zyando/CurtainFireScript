# -*- coding: utf-8 -*-

#上方向に1つ60フレーム後に消える弾を発射するスクリプト

shot = EntityShot(WORLD, "S", 0xFF0000)

shot.Velocity = Vector3(0, 1, 0)

#寿命を設定する
shot.LivingLimit = 60

shot()