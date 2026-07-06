# #Clean folder for testing
import sys, shutil
if len(sys.argv)<2 or  "y" not in sys.argv[1]:
    print("Do not run this")
    exit() 
if "v" in sys.argv[1]:
    try:
        shutil.rmtree("videos")
    except:
        pass
try:
    shutil.rmtree(".config")
except:
    pass
try:
    shutil.rmtree("yt-dlp")
except:
    pass
try:
    shutil.rmtree("ffmpeg-master-latest-win64-gpl")
except:
    pass