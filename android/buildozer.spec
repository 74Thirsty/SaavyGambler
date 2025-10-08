[app]
title = SaavyGambler
description = Simple modern interface for SaavyGambler insights
package.name = gambler
package.domain = org.saavygambler
author = SaavyGambler Team
source.dir = ..
source.include_exts = py,kv,atlas
source.exclude_dirs = tests,.github,__pycache__
version = 0.1.0
requirements = python3,kivy==2.2.1,kivymd,httpx,pydantic
orientation = portrait
fullscreen = 0
android.api = 33
android.minapi = 24
android.archs = arm64-v8a,armeabi-v7a
android.permissions = INTERNET
log_level = 2
main = gui_main.py

# Configure release signing before uploading to the Play Store. Leave these
# blank for debug builds and populate them via environment templating or manual
# edits prior to running ``buildozer android release``.
android.release_keystore =
android.release_keyalias =
android.keystore_password =
android.keyalias_password =

[buildozer]
warn_on_root = 1
log_level = 2
