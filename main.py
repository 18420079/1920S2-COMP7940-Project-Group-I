from __future__ import unicode_literals

import os
import sys
import redis
import pathlib

from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)

from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, VideoMessage, VideoSendMessage, FileMessage, StickerMessage, StickerSendMessage
)
from linebot.utils import PY3

redisHOST = "redis-19674.c92.us-east-1-3.ec2.cloud.redislabs.com"
redisPWD = "WYi2cEXgyPf4qFB5sLBw6qjiEmGwekQH"
redisPORT = "19674" 

redis1 = redis.Redis(host = redisHOST, password = redisPWD, port = redisPORT)

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)

# obtain the port that heroku assigned to this app.
heroku_port = os.getenv('PORT', None)

if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if isinstance(event.message, TextMessage):
            handle_TextMessage(event)
        if isinstance(event.message, ImageMessage):
            handle_ImageMessage(event)
        if isinstance(event.message, VideoMessage):
            handle_VideoMessage(event)
        if isinstance(event.message, FileMessage):
            handle_FileMessage(event)
        if isinstance(event.message, StickerMessage):
            handle_StickerMessage(event)

        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

    return 'OK'
    
def list_files(dir):                                                                                                  
    r = []                                                                                                            
    subdirs = [x[0] for x in os.walk(dir)]                                                                            
    for subdir in subdirs:                                                                                            
        files = os.walk(subdir).__next__()[2]                                                                             
        if (len(files) > 0):                                                                                          
            for file in files:                                                                                        
                r.append(subdir + "/" + file)                                                                         
    return r 
    
def handle_Measure(event,state):
    try:
        redis1.set(event.source.user_id,"1")    
        redis1.incr("state_" + event.source.user_id)
        currentstate = int(redis1.get("state_" + event.source.user_id))
        
        originalContentUrl = str(redis1.hget("measure",str(currentstate)), "utf-8")
        previewImageUrl = str(redis1.hget("measure", str(currentstate) + "s"), "utf-8")
        
        #print(originalContentUrl)
        #print(type(originalContentUrl))
        #print(os.path.exists(originalContentUrl))
        #print(previewImageUrl)
        #print(type(previewImageUrl))
        #print(os.path.exists(previewImageUrl))
        #print(pathlib.Path().absolute())        
        
        m = VideoSendMessage(original_content_url=originalContentUrl,preview_image_url=previewImageUrl)
        
        if redis1.hlen("measure") > currentstate * 2:
            line_bot_api.reply_message(event.reply_token,[m,TextSendMessage("More?")])
        else:
            redis1.delete(event.source.user_id)
            redis1.delete("state_" + event.source.user_id)
            line_bot_api.reply_message(event.reply_token,[m,TextSendMessage("Thanks for watching and take care!")])
              
        return ""
    except Exception as e:
        print("error")
        print(str(e))
        redis1.delete(event.source.user_id)
        redis1.delete("state_" + event.source.user_id)
        return "Server connection fail, please try again later"           

def handle_Mask(event,state):
    try:
        redis1.set(event.source.user_id,"2")
        redis1.set("state_" + event.source.user_id,state)
        
        if state == 0:
            return "Please input district, or \"No\" to exit"
        elif state ==  1:
            taradd = event.message.text.lower().replace(" ","").strip()
            if event.message.text == "*":
                rvaddarr = redis1.hgetall("mask")
                replytext = "Shop still have mask as below:"
                replyarr = []
                messagecount = 0
                for x in rvaddarr:
                    if x + b'n' in rvaddarr and x + b's' in rvaddarr and int(rvaddarr[x + b's']) > 0:
                        if len(replytext + "\n" + str(rvaddarr[x + b'n'], "utf-8") + " : " + str(rvaddarr[x], "utf-8")) >= 2000:
                            if messagecount >= 3:
                                break
                            replyarr.append(TextSendMessage(replytext))
                            messagecount += 1
                            replytext = ""
                        replytext += "\n" + str(rvaddarr[x + b'n'], "utf-8") + " : " + str(rvaddarr[x], "utf-8")
                replyarr.append(TextSendMessage(replytext))
                replyarr.append(TextSendMessage("Thanks for the query and take care!"))

                redis1.delete(event.source.user_id)
                redis1.delete("state_" + event.source.user_id)
                line_bot_api.reply_message(event.reply_token,replyarr)                
            else:
                rvadd = redis1.hget("mask", taradd)
                if rvadd is None:
                    return "District not found, Do you want to search for other district?"
                rvnum = redis1.hget("mask", taradd + "s")
                if rvnum is None:
                    return "District not found, Do you want to search for other district?"
                line_bot_api.reply_message(event.reply_token,
                                           [
                                               TextSendMessage("Addess of selling mask in " + event.message.text.strip() + " is " + str(rvadd, "utf-8") + " with " + str(int(rvnum)) + " of Box in stock"),
                                               TextSendMessage("Do you want to search for other district?")
                                           ])
        return ""
    except Exception as e:
        print("error")
        print(str(e))
        redis1.delete(event.source.user_id)
        redis1.delete("state_" + event.source.user_id)
        raise
        return "Server connection fail, please try again later"     

# Handler function for Text Message
def handle_TextMessage(event):
    print(event.message.text)
    #msg = 'You said: "' + event.message.text + '" '    
    currentmethod = redis1.get(event.source.user_id)
    msg = ""
    if currentmethod is None:    
        if event.message.text.lower() == "measure":
            msg = handle_Measure(event,0)
        elif event.message.text.lower() == "mask":
            msg = handle_Mask(event,0);
        else:
            msg = "Please input \"Measure\" or \"Mask\" to getting service"
    elif currentmethod == "1":
        if event.message.text.lower() == "yes" or event.message.text.lower() == "more":
            msg = handle_Measure(event,5)
        elif event.message.text.lower() == "no":
            redis1.delete(event.source.user_id)
            redis1.delete("state_" + event.source.user_id)
            msg = "Thanks for watching and take care!"
        else:
            msg = "Please input \"Yes\", \"More\" or \"No\""
    else:
        if event.message.text.lower() == "yes" or event.message.text.lower() == "more":
            msg = handle_Mask(event,0)
        elif event.message.text.lower() == "no":
            redis1.delete(event.source.user_id)
            redis1.delete("state_" + event.source.user_id)
            msg = "Thanks for the query and take care!"
        else:
            msg = handle_Mask(event, 1)
    
    if msg != "":
        print(msg)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(msg)
        )

# Handler function for Sticker Message
def handle_StickerMessage(event):
    line_bot_api.reply_message(
	event.reply_token,
	TextSendMessage(text="Please input \"Measure\" or \"Mask\" to getting service")
    )

# Handler function for Image Message
def handle_ImageMessage(event):
    line_bot_api.reply_message(
	event.reply_token,
	TextSendMessage(text="Please input \"Measure\" or \"Mask\" to getting service")
    )

# Handler function for Video Message
def handle_VideoMessage(event):
    line_bot_api.reply_message(
	event.reply_token,
	TextSendMessage(text="Please input \"Measure\" or \"Mask\" to getting service")
    )

# Handler function for File Message
def handle_FileMessage(event):
    line_bot_api.reply_message(
	event.reply_token,
	TextSendMessage(text="Please input \"Measure\" or \"Mask\" to getting service")
    )

if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(host='0.0.0.0', debug=options.debug, port=heroku_port)
