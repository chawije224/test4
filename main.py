from mpegdash.parser import MPEGDASHParser
from button_build import ButtonMaker
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters
import requests
from getKeys import getKeyss
from getPSSH import getPSSHs
from time import sleep
from html import parser
from download import down, decr
import os, glob
from pyrogram import Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from threading import Lock
from help import *
from l3 import WV_Function
from getUrls import getUrl

dict = {}

download_dict = {}
download_dict_lock = Lock()

butn = InlineKeyboardMarkup([[InlineKeyboardButton("CC", url="https://t.me/testmpd_bot")]])

client = Client(
    name="pyrogrammm",
    api_id=17872567,
    api_hash='6aea250af9d83f85a9adc8e34705415a',
    bot_token='5512093783:AAGT6cMNJFhPioM2VADELGMdD1zGucT35G8',
    no_updates=True,
    #ipv6=True
)

app = ApplicationBuilder().token("5512093783:AAGT6cMNJFhPioM2VADELGMdD1zGucT35G8").concurrent_updates(True).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['isEdmx'] = False
    await update.message.reply_text("use /help for further help", quote=True)

async def edmx(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['isEdmx'] = False
    try:
        working_dir = os.getcwd() + "/working_dir"
        os.chdir(working_dir)
    except:
        pass
    mpd = update.message.text.split()[1]
    try:
        txt = requests.get(mpd).text
    except:
        await update.message.reply_text("Invalid MPD link", quote=True)
        return
    with open('manifest.mpd', 'w') as f:
        f.write(txt)
    token = update.message.text.split()[-1]
    pssh = getPSSHs(mpd)
    try:
        await update.message.reply_html(f'<b>PSSH: </b><code>{pssh}</code>', quote=True)
    except: pass
    # headers['x-axdrm-message'] = token
    try:
        keys = WV_Function(pssh, token)
    except:
        await update.message.reply_text("Input error", quote=True)
        return
    v, a = getUrl(mpd)
    global msg
    msg = update.message
    message1 = await msg.reply_html('<b>Keys are being extracted . </b>', quote=True)
    sleep(0.5)
    message1 = await message1.edit_text('<b>Keys are being extracted . .</b>', parse_mode='HTML')
    sleep(0.5)
    message1 = await message1.edit_text('<b>Keys are being extracted . . .</b>', parse_mode='HTML')
    sleep(0.25)
    if keys is not None:
            await message1.edit_text(f'''
<b>Extracted Keys:</b>

<code>--key {keys}</code>        
        ''', parse_mode='HTML')
    sleep(2)
    user = msg.from_user.id
    try:
        dict[user] += 1
    except:
        dict.update({user: 1})
    context.user_data['isEdmx'] = True
    print(dict)
    await message1.edit_text("<i>Downloading...</i>", parse_mode='HTML')
    result = await down(v=v, a=a, isEdmx=True, msg=message1)
    context.user_data['isEdmx'] = False
    if result == 'OK':
        await message1.edit_text("<i>Decrypting video...</i>", parse_mode='HTML')
        result2 = await decr(keys, msg=message1, isEdmx=True)
        if result2 == 'OK':
            await message1.edit_text("<i>Uploading video...</i>", parse_mode='HTML')
            await send()
            await message1.delete()

async def help(update, context):
    context.user_data['isEdmx'] = False
    await update.message.reply_text('''
<b>Send them in this format:</b>

[<code>mpd_link</code>] [<code>license_url</code>]
    
<b>Eg:</b>
<i>https://cdn.bitmovin.com/content/assets/art-of-motion_drm/mpds/11331.mpd https://cwip-shaka-proxy.appspot.com/no_auth</i>  
''', parse_mode="HTML", quote=True)

async def calls(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data.split('_')[1] == 'vid':
        context.user_data['h'] = query.data.split('_', maxsplit=3)[-2]
        global vid_id
        vid_id = query.data.split('_', maxsplit=3)[-1]
        await query.edit_message_text('''<b>
Chose audio quality for download
    </b>''', parse_mode='HTML', reply_markup=aud)
    else:
        aud_id = query.data.split('_', maxsplit=2)[-1]
        await query.edit_message_text("<i>Downloading...</i>", parse_mode='HTML')
        user = query.from_user.id
        try:
            dict[user] += 1
        except:
            dict.update({user: 1})
        print(dict)
        if context.user_data['isEdmx']:
            vi,au = getUrl(mpdURL, context.user_data['h'])
            result = await down(v=vi, a=au, isEdmx=True, msg=query)
        else:
            result = await down(vid_id, aud_id, mpdURL, user, msg=query)
        context.user_data['isEdmx'] = False
        if result == 'OK':
            await query.edit_message_text("<i>Decrypting video and audio files...</i>", parse_mode='HTML')
            result2 = await decr(keys, query)
            if result2 == 'OK':
                await query.edit_message_text("<i>Uploading video...</i>", parse_mode='HTML')
                await send()
                await query.delete_message()


def cleanup(path):
    leftover_files = glob.glob(path + '/*.mp4', recursive=True)
    mpd_files = glob.glob(path + '/*.mpd', recursive=True)
    leftover_files = leftover_files + mpd_files
    for file_list in leftover_files:
        try:
            os.remove(file_list)
        except OSError:
            print(f"Error deleting file: {file_list}")

async def send():
    try:await client.start()
    except: pass
    await client.send_video(msg.chat_id, open('final.mp4', 'rb'),supports_streaming=True, reply_to_message_id=msg.id, reply_markup=butn, caption='Final.mp4')
    try:await client.stop()
    except:pass
    cleanup(os.getcwd())

async def getButtons(message):
    uid = message.from_user.id
    mpd = MPEGDASHParser.parse("manifest.mpd")
    v_buttons = ButtonMaker()
    a_buttons = ButtonMaker()
    for period in mpd.periods:
        for adapt_set in period.adaptation_sets:
            content_type = adapt_set.mime_type
            lst = []
            try:
                for i in adapt_set.representations:
                    lst.append(i.mime_type)
                print(lst)
            except:
                lst = []
            if adapt_set.mime_type == "video/mp4" or adapt_set.content_type == 'video':
                for h in adapt_set.representations:
                    print(h.height)
                    v_buttons.sbutton(f"{h.height}p", f"{uid}_vid_{h.height}_{h.id}")
            elif adapt_set.mime_type == "audio/mp4" or adapt_set.content_type == 'audio':
                for q in adapt_set.representations:
                    a_buttons.sbutton(f"{q.id}", f"{uid}_aud_{q.id}")
            elif ('video/mp4' or 'video') in lst:
                for h in adapt_set.representations:
                    print(h.height)
                    v_buttons.sbutton(f"{h.height}p", f"{uid}_vid_{h.height}_{h.id}")
            elif ('audio/mp4' or 'audio') in lst:
                for q in adapt_set.representations:
                    a_buttons.sbutton(f"{q.id}", f"{uid}_aud_{q.id}")
    vid = v_buttons.build_menu(1)
    # await message.reply_html("<b>Chose video quality</b>", reply_markup=vid)
    global aud
    aud = a_buttons.build_menu(1)
    # await message.reply_html("<b>Chose audio quality</b>", reply_markup=aud)
    return vid, aud

async def input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['isEdmx'] = False
    global msg
    msg = update.message
    if msg.text[-3:] == "mpd":
        await msg.reply_text('''
<b>Send them in this format:</b>

[<code>mpd_link</code>] [<code>license_url</code>]
    
<b>Eg:</b>
<i>https://cdn.bitmovin.com/content/assets/art-of-motion_drm/mpds/11331.mpd https://cwip-shaka-proxy.appspot.com/no_auth</i>
''', parse_mode="HTML", quote=True)
    elif len(str(msg.text).split(maxsplit=1)) == 2:
        # message.reply('<b>Keys are being extracting . . .</b>')
        message1 = await msg.reply_html('<b>Keys are being extracted . </b>', quote=True)
        sleep(0.5)
        message1 = await message1.edit_text('<b>Keys are being extracted . .</b>', parse_mode='HTML')
        sleep(0.5)
        message1 = await message1.edit_text('<b>Keys are being extracted . . .</b>', parse_mode='HTML')
        sleep(0.25)
        global mpdURL
        mpdURL, lic = str(msg.text).split(maxsplit=1)
        try:
            manifest = requests.get(mpdURL).text
            with open("manifest.mpd", 'w') as manifest_handler:
                manifest_handler.write(manifest)
        except:
            return await message1.edit_text('<b>Input error! use /help</b>', parse_mode='HTML')
        pssh = getPSSHs(mpdURL)
        try:
            await update.message.reply_html(f'<b>PSSH: </b><code>{pssh}</code>', quote=True)
        except:
            pass
        global keys
        keys = await getKeyss(pssh=pssh, license=lic)
        if keys is not None:
            await message1.edit_text(f'''
<b>Extracted Keys:</b>

<code>--key {keys}</code>        
        ''', parse_mode='HTML')
        else:
            return await message1.edit_text('<b>Still that type is Not Supported</b>', parse_mode='HTML')
        sleep(1)
        if str(mpdURL).split('/')[2] == 'video.lk.databoxtech.com':
            context.user_data['isEdmx'] = True
        listener = MainHelper(app.bot, msg)
        vid, aud = await context.application.create_task(getButtons(msg))
        await message1.edit_text('''<b>
Chose video quality for download:
        </b>''', parse_mode='HTML', reply_markup=vid)

    else:
        await msg.reply_html('<b>Syntax error! use /help</b>', quote=True)
        return

app.add_handler(CommandHandler("start", start))
app.add_handler((CommandHandler("help", help)))
app.add_handler((CommandHandler('edmx', edmx)))
app.add_handler(MessageHandler(filters.ChatType.PRIVATE, input))
app.add_handler(CallbackQueryHandler(calls))


app.run_polling()