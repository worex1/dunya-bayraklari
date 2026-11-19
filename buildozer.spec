[app]
title = Dünya Bayrakları
package.name = dunyabayraklari
package.domain = org.worex1
source.dir = .
source.include_exts = py,png,jpg,kv,json
version = 0.2
requirements = python3,kivy,requests
android.permissions = INTERNET
orientation = portrait
fullscreen = 0
icon.filename = %(source.dir)s/uygulama_ikonu_kaynak.png
android.minapi = 21
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
