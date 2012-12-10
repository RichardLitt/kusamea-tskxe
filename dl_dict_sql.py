#!/usr/bin/env python3
import urllib.request
import shutil

with urllib.request.urlopen("http://eanaeltu.learnnavi.org/dicts/NaviData.sql") as response, open("dict.sql", "wb") as f:
	shutil.copyfileobj(response, f)
