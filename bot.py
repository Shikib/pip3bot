from telegram import Updater
from googlesearch import GoogleSearch
from googleapiclient.discovery import build
from random import random

updater = Updater(token='178314829:AAGcHaT7n_q3USrSIcq8YX_eVrizfyLs64Y')

dispatcher = updater.dispatcher

def echo(bot, chat_id, text):
  bot.sendMessage(chat_id=chat_id, text=text)

def caps(bot, chat_id, text):
  bot.sendMessage(chat_id=chat_id, text=text.upper())

def google(bot, chat_id, text):
  gs = GoogleSearch(text)
  message_str = "\n\r".join(["%s -- %s" % (gsr['url'], gsr['title']) for gsr in gs.top_results()]).replace("<b>", "").replace("</b>", "")
  bot.sendMessage(chat_id=chat_id, text=message_str)

service = build("customsearch", "v1", developerKey="AIzaSyBqkks-ZHiGzsGkYfPlDbOFJJPlDR4Xu9A")

def img(bot, chat_id, text):
  res = service.cse().list(q=text, cx="015921083071919057855:exifcoru2nc", searchType="image").execute()
  print res['items']
  print res['items'][int(random() * 10)]
  print res['items'][int(random() * 10)]['link']
  bot.sendMessage(chat_id=chat_id, text=res['items'][int(random() * 10)]['link'])

triggers = {}

def trigger(bot, chat_id, text):
  best_trigger = ''
  for trig in triggers.keys():
    if trig in text and len(trig) > len(best_trigger):
      best_trigger = trig

  if best_trigger:
    bot.sendMessage(chat_id=chat_id, text=triggers[best_trigger])

def set_trigger(text):
  global triggers
  key, val = [strng.strip() for strng in text.split("==>")]

  if len(key) > 1 and len(val) > 1:
    triggers[key] = val 

def show_triggers(bot, chat_id):
  global triggers

  text = "trigger warnings: %s" % (", ".join(triggers.keys()))
  bot.sendMessage(chat_id=chat_id, text=text) 

def magic8ball(bot, chat_id):
  replies = ['Signs point to yes',
          'Without a doubt',
          'You may rely on it',
          'Do not count on it',
          'Looking good',
          'Cannot predict now',
          'It is decidedly so',
          'Outlook not so good']

  bot.sendMessage(chat_id=chat_id, text=replies[int(random() * len(replies))])
  
# all messages to the bot come here for processing
def main(bot, update):
  message_text = update.message.text
  chat_id = update.message.chat_id
  
  words = message_text.split()
  cmd = words[0]
  text = ' '.join(words[1:]) if len(words) > 1 else ''

  if cmd == '!img':
    img(bot, chat_id, text)
  elif cmd == '!echo':
    echo(bot, chat_id, text)
  elif cmd == '!caps':
    caps(bot, chat_id, text)
  elif cmd == '!google':
    google(bot, chat_id, text)
  elif cmd == '!magic8ball':
    magic8ball(bot, chat_id)
  elif "==?" == message_text:
    show_triggers(bot, chat_id)
  elif "==>" in message_text:
    set_trigger(message_text)
  else:
    trigger(bot, chat_id, message_text)

dispatcher.addTelegramMessageHandler(main)

updater.start_polling()
