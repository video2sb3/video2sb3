import os
import shutil
import ffmpeg
import hashlib
import sys

# Ensure the script receives an argument for the video file
if len(sys.argv) != 2:
    print("Usage: python second_script.py <video_file>")
    exit(1)

# Get the video file path from the command-line argument
vid = sys.argv[1]

# Check if the video file exists
if not os.path.exists(vid):
    print(f"Video file '{vid}' not found!")
    exit(1)

# Proceed with the extraction process
try:
    if os.path.exists("temp"):
        shutil.rmtree("temp")
    os.makedirs("temp")
    print("Extracting video frames and audio...")

    # Check if the video file has an audio stream
    a = ffmpeg.probe(vid, select_streams="a")["streams"]
    if a:
        ffmpeg.input(vid).output("temp/83c36d806dc92327b9e7049a565c6bff.mp3", loglevel="quiet").run()

    ffmpeg.input(vid).output("temp/%d.jpg", vf="fps=30,scale=960:720", loglevel="quiet").run()

    print("Hashing frames and creating project.json...")
    frame = 1
    json = ""
    while True:
        if not os.path.exists(f"temp/{frame}.jpg"):
            break
        id = hashlib.md5(str(frame).encode()).hexdigest()
        json += f'{{"name":"{frame}","bitmapResolution":2,"dataFormat":"jpg","assetId":"{id}","md5ext":"{id}.jpg","rotationCenterX":480,"rotationCenterY":360}},'
        os.rename(f"temp/{frame}.jpg", f"temp/{id}.jpg")
        frame += 1

    json = f'{{"targets":[{{"isStage":true,"name":"Stage","variables":{{}},"lists":{{}},"broadcasts":{{}},"blocks":{{}},"comments":{{}},"currentCostume":0,"costumes":[{{"name":"backdrop1","dataFormat":"svg","assetId":"cd21514d0531fdffb22204e0ec5ed84a","md5ext":"cd21514d0531fdffb22204e0ec5ed84a.svg","rotationCenterX":240,"rotationCenterY":180}}],"sounds":[],"volume":100,"layerOrder":0,"tempo":60,"videoTransparency":50,"videoState":"on","textToSpeechLanguage":null}},{{"isStage":false,"name":"Video","variables":{{}},"lists":{{}},"broadcasts":{{}},"blocks":{{"d":{{"opcode":"event_whenflagclicked","next":"a","parent":null,"inputs":{{}},"fields":{{}},"shadow":false,"topLevel":true,"x":459,"y":281}},"b":{{"opcode":"sound_play","next":"c","parent":"a","inputs":{{"SOUND_MENU":[1,"e"]}},"fields":{{}},"shadow":false,"topLevel":false}},"e":{{"opcode":"sound_sounds_menu","next":null,"parent":"b","inputs":{{}},"fields":{{"SOUND_MENU":["audio",null]}},"shadow":true,"topLevel":false}},"a":{{"opcode":"looks_switchcostumeto","next":"b","parent":"d","inputs":{{"COSTUME":[1,"f"]}},"fields":{{}},"shadow":false,"topLevel":false}},"f":{{"opcode":"looks_costume","next":null,"parent":"a","inputs":{{}},"fields":{{"COSTUME":["1",null]}},"shadow":true,"topLevel":false}},"c":{{"opcode":"control_repeat","next":null,"parent":"b","inputs":{{"TIMES":[1,[6,"%s"]]}},"fields":{{}},"shadow":false,"topLevel":false}},"g":{{"opcode":"looks_nextcostume","next":null,"parent":"c","inputs":{{}},"fields":{{}},"shadow":false,"topLevel":false}}}}],"comments":{{}},"currentCostume":0,"costumes":[{frame}]}}'

    json += '],"sounds":['

    if a:
        json += '{"name":"audio","assetId":"83c36d806dc92327b9e7049a565c6bff","dataFormat":"mp3","md5ext":"83c36d806dc92327b9e7049a565c6bff.mp3"}'

    with open("temp/project.json", "w") as file:
        file.write(json + '],"volume":100,"layerOrder":1,"visible":true,"x":0,"y":0,"size":100,"direction":90,"draggable":false,"rotationStyle":"all around"}],"monitors":[],"extensions":[],"meta":{"semver":"3.0.0","vm":"0.2.0","agent":""}}')

    print("Zipping to .sb3...")
    shutil.make_archive("temp", "zip", "temp")
    shutil.rmtree("temp")
    os.rename("temp.zip", "result.sb3")
    print("Operation successfully completed.")

except Exception as e:
    print(f"An error occurred: {e}")
