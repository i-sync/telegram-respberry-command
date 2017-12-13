#!/usr/bin/env python3
# _*_ coding: utf-8 _*_

import os
import os.path
import subprocess
import signal
import sys
import logging
logfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log.txt')
#logging.basicConfig(filename = logfile, level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
import telegram
import telegram.utils.request
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters

from config import Config
from config import objectview



#req = telegram.utils.request.Request(proxy_url= Config.proxy)
#bot = telegram.Bot(Config.token, request= req)
bot = telegram.Bot(Config.token)
def command_process(bot, update):
    #print(type(update))
    text = update.message.text
    logging.info(text)
    if text.startswith('/help') or text.startswith('/start'):
        custom_keyboard = [['bash run.sh status', 'bash run.sh start'], ['bash run.sh restart', 'bash run.sh stop']]
        reply_keyboard_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True)
        bot.send_message(chat_id=update.message.chat_id, text= 'Please Select Command', reply_markup = reply_keyboard_markup)
    else:
        bot.send_message(chat_id= update.message.chat_id, text = 'sorry, i can\'t understand what\'s your mean...')
    '''    
    elif text.startswith('/weather'):
        bot.send_message(chat_id=update.message.chat_id, text= common.get_weather())
    elif text.startswith('/gif'):
        url = common.get_random_gif()
        if url is None:
            bot.send_message(chat_id=update.message.chat_id, text= 'get random gif failed, please try again later...')
        else:
            bot.send_video(chat_id=update.message.chat_id, video = url)
    elif text.startswith('/joke'):
        bot.send_message(chat_id=update.message.chat_id, text= common.get_random_joke())
    #elif text.startswith('/message'):
    #    bot.send_message(chat_id=update.message.chat_id, text = json.dumps(update.message))
    #    logging.info(update.message)
    elif text.startswith('/me'):
        bot_obj = bot.get_me()
        bot_info = {'id': bot_obj.id, 'username': bot_obj.username, 'first_name': bot_obj.first_name, 'last_name': bot_obj.last_name, 'type': bot_obj.type}
        bot.send_message(chat_id=update.message.chat_id, text= json.dumps(bot_info))
    '''

def text_process(bot, update):
    #logging.info(update.message)
    #{'message_id': 106, 'date': 1513139810, 'chat': {'id': 376585058, 'type': 'private', 'username': 'asynchronized', 'first_name': 'synchronize'}, 'text': 'Ll', 'entities': [], 'caption_entities': [], 'photo': [], 'new_chat_members': [], 'new_chat_photo': [], 'delete_chat_photo': False, 'group_chat_created': False, 'supergroup_chat_created': False, 'channel_chat_created': False, 'from': {'id': 376585058, 'first_name': 'synchronize', 'is_bot': False, 'username': 'asynchronized', 'language_code': 'en'}, 'new_chat_member': None}
    logging.info(str(update.message))

    #check message user
    if update.message.chat_id in Config.user_id:
        try:
            command = update.message.text.lower()
            res = process_command(command)
            bot.send_message(chat_id= update.message.chat_id, text = res.stdout if res.returncode == 0 else res.stderr) 
        except Exception as e:
            bot.send_message(chat_id = update.message.chat_id, text = str(e))
    else:
        bot.send_message(chat_id = update.message.chat_id, text = "Sorry, you don't have permisssion to do this ...")

def photo_process(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Thank for your photo message...')

def audio_process(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Thank for your audio message...')

def video_process(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Thank for your vedio message...')

def default_process(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Thank for your message...')

def process_command(command):
    #print(command)
    #command = command.strip([' ', '\n'])
    logging.info(command)
    process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return objectview({"returncode": process.returncode, "stdout": process.stdout.decode('utf-8'), "stderr": process.stderr.decode('utf-8')})

def start():
    updater = Updater(bot = bot)

    updater.start_polling()

    dispacther = updater.dispatcher

    #handler
    command_handler = CommandHandler(Config.command_list, command_process)
    text_handler = MessageHandler(Filters.text, text_process)
    #photo_handler = MessageHandler(Filters.photo, photo_process)
    #audio_handler = MessageHandler(Filters.audio | Filters.voice | Filters.forwarded & Filters.audio | Filters.forwarded & Filters.voice, audio_process)
    #video_handler = MessageHandler(Filters.video, video_process)

    dispacther.add_handler(command_handler)
    dispacther.add_handler(text_handler)
    #dispacther.add_handler(photo_handler)
    #dispacther.add_handler(audio_handler)
    #dispacther.add_handler(video_handler)


def signal_handler(signal, frame):
    logging.info("Ctrl + C was pressed , stop ...")
    sys.exit(0)

if __name__ == '__main__':    
    #signal.signal(signal.SIGINT, signal_handler)

    #change directory
    os.chdir(Config.des_path)
    start()
    #signal.pause()