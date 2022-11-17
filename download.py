import os
from telegram import *
from telegram.ext import *
from subprocess import Popen, PIPE
from time import sleep

async def down(vid=None, aid=None, url=None, uid=None, v=None, a=None, isEdmx = False, msg=None):
    if not isEdmx:
        try:
            print(vid, aid)
            try:
                working_dir = os.getcwd() + "\working_dir"
                os.chdir(working_dir)
            except:
                pass
            f = open('new.txt', 'w')
            er = open('error.txt', 'w')
            Popen(f"yt-dlp -f {vid} --allow-unplayable-formats {url} -o evideo.mp4", shell=True, stdout=f, stderr=er)
            await msgs(msg)
            Popen(f"yt-dlp -f {aid} --allow-unplayable-formats {url} -o eaudio.mp4", shell=True, stdout=f, stderr=er)
            await msgs(msg)
            return 'OK'
        except Exception as e:
            return
    else:
        try:
            try:
                working_dir = os.getcwd() + "\working_dir"
                os.chdir(working_dir)
            except:
                pass
            f = open('new.txt', 'w')
            er = open('error.txt', 'w')
            Popen(f"yt-dlp {v} -o evideo.mp4", shell=True, stdout=f, stderr=er)
            await msgs(msg)
            Popen(f"yt-dlp {a} -o eaudio.mp4", shell=True, stdout=f, stderr=er)
            await msgs(msg)
            return 'OK'
        except Exception as e:
            return

async def decr(keys, msg, isEdmx = False):
    try:
        try:
            working_dir = os.getcwd() + "\working_dir"
            os.chdir(working_dir)
        except:
            pass
        os.system(f"mp4decrypt --key {keys} evideo.mp4 dvideo.mp4")
        os.system(f"mp4decrypt --key {keys} eaudio.mp4 daudio.mp4")
        if isEdmx:
            await msg.edit_text("<i>Merging video, audio files...</i>", parse_mode='HTML')
        else:
            await msg.edit_message_text("<i>Merging video, audio files...</i>", parse_mode='HTML')
        os.system("ffmpeg -y -i daudio.mp4 -i dvideo.mp4 -acodec copy -vcodec copy -fflags +bitexact final.mp4")
        return "OK"
    except:
        return

async def msgs(msg):
    ntxt = 2
    while True:
        r = open('new.txt', 'r')
        
        try:
            txt = r.readlines()[-1]
            if txt != ntxt:
                await msg.edit_text(f"<code>{txt}</code>", parse_mode='HTML')
                ntxt = txt
                sleep(3)
            else:
                break
        except Exception as e:
            #print(e)
            pass