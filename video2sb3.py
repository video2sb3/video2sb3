#       _     _           ____      _    _____ 
#__   _(_) __| | ___  ___|___ \ ___| |__|___ / 
#\ \ / / |/ _` |/ _ \/ _ \ __) / __| '_ \ |_ \ 
# \ V /| | (_| |  __/ (_) / __/\__ \ |_) |__) |
#  \_/ |_|\__,_|\___|\___/_____|___/_.__/____/ 
# Run this file to start the program!

import os
import shutil
import ffmpeg
import hashlib

vid = input("Input your video here! ")
if vid.startswith("'"):
    vid = vid [1:-1]
if os.path.exists("temp"):
    shutil.rmtree("temp")
os.makedirs("temp")
(
    ffmpeg.input(vid)
    .output("temp/83c36d806dc92327b9e7049a565c6bff.mp3") # Scratch is really strict about hashing filenames
    .run()
)
(
    ffmpeg.input(vid)
    .output("temp/%d.jpg", vf="fps=30,scale=960:720")
    .run()
)
print("Hashing frames and creating project.json...")
frame = 1
json = ""
while True:
    if not os.path.exists("temp/%s.jpg" % frame):
        break
    id = hashlib.md5(str(frame).encode()).hexdigest()
    json += '{"name":"%s","bitmapResolution":2,"dataFormat":"jpg","assetId":"%s","md5ext":"%s.jpg","rotationCenterX":480,"rotationCenterY":360},' % (frame, id, id)
    os.rename("temp/%s.jpg" % frame,"temp/%s.jpg" % id)
    frame += 1
json = ('{"targets":[{"isStage":true,"name":"Stage","variables":{},"lists":{},"broadcasts":{},"blocks":{},"comments":{},"currentCostume":0,"costumes":[{"name":"backdrop1","dataFormat":"svg","assetId":"cd21514d0531fdffb22204e0ec5ed84a","md5ext":"cd21514d0531fdffb22204e0ec5ed84a.svg","rotationCenterX":240,"rotationCenterY":180}],"sounds":[],"volume":100,"layerOrder":0,"tempo":60,"videoTransparency":50,"videoState":"on","textToSpeechLanguage":null},{"isStage":false,"name":"Video","variables":{},"lists":{},"broadcasts":{},"blocks":{"d":{"opcode":"event_whenflagclicked","next":"a","parent":null,"inputs":{},"fields":{},"shadow":false,"topLevel":true,"x":459,"y":281},"b":{"opcode":"sound_play","next":"c","parent":"a","inputs":{"SOUND_MENU":[1,"e"]},"fields":{},"shadow":false,"topLevel":false},"e":{"opcode":"sound_sounds_menu","next":null,"parent":"b","inputs":{},"fields":{"SOUND_MENU":["audio",null]},"shadow":true,"topLevel":false},"a":{"opcode":"looks_switchcostumeto","next":"b","parent":"d","inputs":{"COSTUME":[1,"f"]},"fields":{},"shadow":false,"topLevel":false},"f":{"opcode":"looks_costume","next":null,"parent":"a","inputs":{},"fields":{"COSTUME":["1",null]},"shadow":true,"topLevel":false},"c":{"opcode":"control_repeat","next":null,"parent":"b","inputs":{"TIMES":[1,[6,"%s"]],"SUBSTACK":[2,"g"]},"fields":{},"shadow":false,"topLevel":false},"g":{"opcode":"looks_nextcostume","next":null,"parent":"c","inputs":{},"fields":{},"shadow":false,"topLevel":false}},"comments":{},"currentCostume":0,"costumes":[' % str(frame - 1)) + json
file = open("temp/project.json","w")
file.write(json + '],"sounds":[{"name":"audio","assetId":"83c36d806dc92327b9e7049a565c6bff","dataFormat":"mp3","md5ext":"83c36d806dc92327b9e7049a565c6bff.mp3"}],"volume":100,"layerOrder":1,"visible":true,"x":0,"y":0,"size":100,"direction":90,"draggable":false,"rotationStyle":"all around"}],"monitors":[],"extensions":[],"meta":{"semver":"3.0.0","vm":"0.2.0","agent":"","platform":{"name":"TurboWarp","url":"https://turbowarp.org/"}}}')
file.close()
print("Zipping to .sb3...")
shutil.make_archive("temp","zip","temp")
shutil.rmtree("temp")
os.rename("temp.zip","result.sb3")
print("Operation successfully completed.")