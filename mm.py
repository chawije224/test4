from subprocess import Popen, PIPE
from time import sleep

f = open('new.txt', 'w')
er = open('error.txt', 'w')
p = Popen(['yt-dlp', '-f', '2', '--allow-unplayable-formats', 'https://wvm.ezdrm.com/demo/dash/BigBuckBunny_320x180.mpd'], stdout=f, stderr=er)
ntxt = 2
while True:
    r = open('new.txt', 'r')
    
    try:
        txt = r.readlines()[-1]
        if txt != ntxt:
            print(txt)
            ntxt = txt
            sleep(0.5)
        else:
            break
    except:
        pass
    