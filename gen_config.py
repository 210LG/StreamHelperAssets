#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from genericpath import isfile
import json
import os
from posix import listdir
import sys
import tarfile
import subprocess

list = {}

games = [f for f in os.listdir("./games/") if os.path.isdir("./games/"+f)]

for game in games:
    print("Game: "+game)
    path = "./games/"+game+"/"

    try:
        with open(path+"config.json", 'r', encoding='utf-8') as configFile:
            config = json.load(configFile)
            list[game] = {
                "name": config["name"],
                "assets": {}
            }
    except Exception as e:
        print(e)
        continue
    
    assetDirs = [f for f in os.listdir(path) if os.path.isdir(path+f)]
    print("Assets: "+str(assetDirs))

    deleteOldZips = subprocess.Popen(
        ["rm "+path+"*.z*"],
        shell=True
    )
    deleteOldZips.communicate()

    for assetDir in assetDirs:
        path = "./games/"+game+"/"+assetDir+"/"

        try:
            with open(path+"config.json", 'r', encoding='utf-8') as configFile:
                config = json.load(configFile)
                
                _zip = subprocess.Popen([
                    "zip", "-s", "80m", "-r", "-j",
                    "./games/"+game+"/"+assetDir+".zip",
                    "./games/"+game+"/"+assetDir
                ])
                result = _zip.communicate()

                list[game]["assets"][assetDir] = {
                    "name": config.get("name"),
                    "credits": config.get("credits"),
                    "description": config.get("description"),
                    "files": [f for f in os.listdir("./games/"+game+"/") if f.startswith(assetDir+".z")]
                }
        except Exception as e:
            print(e)

with open('assets.json', 'w') as outfile:
    json.dump(list, outfile, indent=4, sort_keys=True)