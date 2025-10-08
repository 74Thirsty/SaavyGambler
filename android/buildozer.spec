[app]
title = StatTrackerPro
description = Simple modern interface for StatTrackerPro insights
package.name = stattrackerpro
package.domain = org.stattrackerpro
author = StatTrackerPro Team
source.dir = ..
source.include_exts = py,kv,atlas
source.exclude_dirs = tests,.github,__pycache__
version = 0.1.0
requirements = python3,kivy==2.2.1,kivymd,httpx,pydantic
orientation = portrait
fullscreen = 0
android.api = 33
android.minapi = 24
android.archs = arm64-v8a
log_level = 2
main = gui_main.py

[buildozer]
warn_on_root = 1
log_level = 2
