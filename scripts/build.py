#!/usr/bin/python

import os
import shutil

src_dir = "."
build_dir = "build"
addon_name = "plugin.audio.soundcloud"
ignore = shutil.ignore_patterns(".*", "scripts", "tests", "venv", "Pipfile*", "__pycache__")

# Clean up
if os.path.exists(build_dir):
    shutil.rmtree(build_dir)

# Copy files
shutil.copytree(".", os.path.join(build_dir, addon_name), False, ignore)

print("Build finished!")
