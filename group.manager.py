#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json 
import requests
import time
import os

TOKEN = "your token"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)
bot_admin='your telegram id'

def get_url(url):
  response = requests.get(url)
  content = response.content.decode("utf8")
  return content

def get_json(url):
  content = get_url(url)
  js = json.loads(content)
  return js

def get_updates():
  url = URL + "getUpdates"
  js = get_json(url)
  url = URL + "getUpdates?offset=-1"
  get_url(url)
  return js

def isChannel(id, offset, length):
  url = URL + "getChatMembersCount?chat_id={}".format(id[offset:length+offset])
  js=get_json(url)
  if js["ok"]==False:
      return False
  if js["ok"]==True:
      return True
def notAdmin(chat_id,user_id):
  url = URL + "getChatMember?chat_id={}&user_id={}".format(chat_id, user_id)
  js = get_json(url)
  status=js["result"]["status"]
  if status=="administrator" or status=="creator" or user_id==bot_admin:
      return False
  else:
      return True

def inter(perm):
  t="به زوری"
  if perm==True:
      t="فعال"
  if perm==False:
      t="غیر فعال"
  return t
def ban_user(chat_id, user_id):
  url = URL + "kickChatMember?chat_id={}&user_id={}".format(chat_id, user_id)
  get_url(url)

def silent_user(chat_id, user_id):
  url = URL + "restrictChatMember?chat_id={}&user_id={}&can_send_messages=false".format(chat_id, user_id)
  get_url(url)

def free_user(chat_id, user_id):
  url = URL + "restrictChatMember?chat_id={}&user_id={}&can_send_messages=true&can_send_messages=true&can_send_media_messages=true&can_send_other_messages=true&can_add_web_page_previews=true".format(chat_id, user_id)
  get_url(url)
def send_message(text, chat_id):
  url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
  get_url(url)
def delete_message(message_id, chat_id):
  url = URL + "deleteMessage?message_id={}&chat_id={}".format(message_id, chat_id)
  get_url(url)
def pin_message(chat_id, message_id):
  url = URL + "pinChatMessage?chat_id={}&message_id={}&disable_notification=false".format(chat_id, message_id)
  get_url(url)

def add_group(chat_id):
  f=open(str(chat_id),"w")
  f.write("0110010")
  f.close()

def str2arg(st):
  return (bool(int(st[0])), bool(int(st[1])), bool(int(st[2])), bool(int(st[3])), bool(int(st[4])), bool(int(st[5])), bool(int(st[6])))

def arg2str(bot, link, channel_id, filters, joinchat, forward_channel, forward_id):
  return str(int(bot))+str(int(link))+str(int(channel_id))+str(int(filters))+str(int(joinchat))+str(int(forward_channel))+str(int(forward_id))

def readarg(chat_id):
  f=open(str(chat_id), "r")
  st=f.read()
  f.close()
  return str2arg(st)

def writearg(chat_id, bot, link, channel_id, filters, joinchat, forward_channel, forward_id):
  f=open(str(chat_id), "w")
  f.write(arg2str(bot, link, channel_id, filters, joinchat, forward_channel, forward_id))
  f.close()

#updates=get_updates()
last_updates={'update_id': 1234567, 'message': {'date': 12345, 'message_id': 123, 'chat': {'type': 'supergroup', 'title': '1234567', 'id': -1234567}, 'text': 'a', 'from': {'language_code': 'en-US', 'first_name': '1234567', 'username': 'acdfghijk', 'is_bot': False, 'id': 1234567}}}


jointext="سلام {} {} به گروه {} خوش اومدی🌷🌹🌷🌹🌷🌹🌷"

bot=False
link=True
channel_id=True
filters=False #not compeleted
joinchat=False

forward_channel=True
forward_id=True


while True:
  time.sleep(2)
  updates=get_updates()
  #reset_updates()
  if updates["ok"]==True:
    upnum=len(updates["result"])
    if upnum!=0:
      if updates["result"][-1]!=last_updates:
        last_updates=updates["result"][-1]
#        print(last_updates)
        groups=os.listdir(os.getcwd())
        for i in list(range(1, upnum)):
          if "callback_query" in updates["result"][i]:
            data=updates["result"][i]["callback_query"]["data"]
            message_id=updates["result"][i]["callback_query"]["message"]["message_id"]
            chat_id=updates["result"][i]["callback_query"]["message"]["chat"]["id"]
            user_id=updates["result"][i]["callback_query"]["from"]["id"]
            if notAdmin(chat_id, user_id)==False:
              if str(chat_id) in groups:
                bot, link, channel_id, filters, joinchat, forward_channel, forward_id=readarg(chat_id)
                if data=="1":
                   link=not(link)
                if data=="2":
                   bot=not(bot)
                if data=="3":
                   forward_channel=not(forward_channel)
                if data=="4":
                   filters=not(filters)
                if data=="5":
                   channel_id=not(channel_id)
                if data=="6":
                   joinchat=not(joinchat)
                if data=="7":
                   forward_id=not(forward_id)
                writearg(chat_id ,bot, link, channel_id, filters, joinchat, forward_channel, forward_id)
                inline_keyboard='chat_id='+str(chat_id)+'&reply_markup={"inline_keyboard":[[{"text":"حذف لینک : '+inter(link)+'","callback_data":"1"}],[{"text":"حذف ربات : '+inter(bot)+'","callback_data":"2"}],[{"text":"قفل فوروارد از کانال : '+inter(forward_channel)+'","callback_data":"3"}],[{"text":"حذف کلمات فیلتر : '+inter(filters)+'","callback_data":"4"}],[{"text":"حذف آی دی کانال : '+inter(channel_id)+'","callback_data":"5"}],[{"text":"پیام خوش آمد گویی : '+inter(joinchat)+'","callback_data":"6"}],[{"text":"قفل فوروارد از افراد : '+inter(forward_id)+'","callback_data":"7"}]]}'
                url= URL + 'editMessageReplyMarkup?message_id=' + str(message_id) + '&' + inline_keyboard
                get_url(url)
                url= URL + 'answerCallbackQuery?callback_query_id=' + updates["result"][i]["callback_query"]["id"] + '&text=تغییرات با موفقیت اعمال شد!' 
                get_url(url)
              else:
                send_message("با سلام گروه شما در این ربات ثبت نشده است برای ثبت گروه خود با یکی از دو آی دی زیر هماهنگ کنید:\n@arsalan_geek \n@arsalan_darvishi",chat_id)
            else:
              url= URL + 'answerCallbackQuery?callback_query_id=' + updates["result"][i]["callback_query"]["id"] + '&text=شما ادمین این گروه نیستید!' 
              get_url(url)
          elif "edited_message" in updates["result"][i]:
            message_id=updates["result"][i]["edited_message"]["message_id"]
            chat_id=updates["result"][i]["edited_message"]["chat"]["id"]
            user_id=updates["result"][i]["edited_message"]["from"]["id"]
            if str(chat_id) in groups:
              bot, link, channel_id, filters, joinchat, forward_channel, forward_id=readarg(chat_id)
              if notAdmin(chat_id, user_id)==True:
                if "entities" in updates["result"][i]["edited_message"]:
                    entnum=len(updates["result"][i]["edited_message"]["entities"])
                    for j in list(range(0, entnum)):
                      offset=updates["result"][i]["edited_message"]["entities"][j-1]["offset"]
                      lenght=updates["result"][i]["edited_message"]["entities"][j-1]["length"]
                      if updates["result"][i]["edited_message"]["entities"][j-1]["type"]=="url" and link==True:
                        delete_message(message_id, chat_id)
                      if updates["result"][i]["edited_message"]["entities"][j-1]["type"]=="mention" and channel_id==True and isChannel(updates["result"][i]["edited_message"]["text"], offset, length)==True:              
                        delete_message(message_id, chat_id)
              if notAdmin(chat_id, user_id)==False:
                if "text" in updates["result"][i]["edited_message"]:
                  text=updates["result"][i]["edited_message"]["text"]
                  if "reply_to_message" in updates["result"][i]["edited_message"]:
                    reply_message_id=updates["result"][i]["edited_message"]["reply_to_message"]["message_id"]
                    reply_user_id=updates["result"][i]["edited_message"]["reply_to_message"]["from"]["id"]
                    if text=="سنجاق":
                      pin_message(chat_id, reply_message_id)     
                    if text=="بن":
                      ban_user(chat_id, reply_user_id)
                      send_message("کاربر با موفقیت بن شد", chat_id)
                    if text=="ساکت":
                      silent_user(chat_id, reply_user_id)
                      send_message("کاربر با موفقیت ساکت شد", chat_id)
                    if text=="آزاد کردن" or text=="ازاد کردن":
                      free_user(chat_id, reply_user_id)
                      send_message("کاربر با موفقیت آزاد شد", chat_id)
                    if text=="حذف پیام":
                      delete_message(message_id, chat_id)
                      delete_message(reply_message_id, chat_id)
                  if text=="تنظیمات":
                    url = URL + 'sendMessage?text=برای تنظیم ربات از کلید های زیر استفاده کنید&' + inline_keyboard
                    get_url(url)
                  if text=="راهنما":
                    send_message("""🗒دستورات ربات :
~~~~~~~~~~~~~~~
🔵بن 
🔺به صورت reply به پیام شخصی که میخواید از گروه حذف و بن بشه 
~~~~~~~~~~~~~~~
🔵ساکت 
🔺به صورت reply به پیام شخصی که میخواید به حالت سکوت بره و نتونه پیام بده
~~~~~~~~~~~~~~~
🔵آزاد کردن 
🔺به صورت reply به پیام شخصی که میخواید تمام محدودیت های اون برداشته بشه (بن و سکوت)
~~~~~~~~~~~~~~~
🔵تنظیمات
🔺وقتی این دستور رو بزنید یک کیبورد شیشه ای براتون باز میشه که میتونید با اون قفل پیام ها رو فعال و غیر فعال کنید""", chat_id)
            else:
              send_message("با سلام گروه شما در این ربات ثبت نشده است برای ثبت گروه خود با یکی از دو آی دی زیر هماهنگ کنید:\n@arsalan_geek \n@arsalan_darvishi",chat_id) 
          elif "message" in updates["result"][i]:
            if updates["result"][i]["message"]["chat"]["type"]=="supergroup":
              message_id=updates["result"][i]["message"]["message_id"]
              chat_id=updates["result"][i]["message"]["chat"]["id"]
              user_id=updates["result"][i]["message"]["from"]["id"]
              group_name=updates["result"][i]["message"]["chat"]["title"]
              if str(chat_id) in groups:
                bot, link, channel_id, filters, joinchat, forward_channel, forward_id=readarg(chat_id)
                inline_keyboard='chat_id='+str(chat_id)+'&reply_markup={"inline_keyboard":[[{"text":"حذف لینک : '+inter(link)+'","callback_data":"1"}],[{"text":"حذف ربات : '+inter(bot)+'","callback_data":"2"}],[{"text":"قفل فوروارد از کانال : '+inter(forward_channel)+'","callback_data":"3"}],[{"text":"حذف کلمات فیلتر : '+inter(filters)+'","callback_data":"4"}],[{"text":"حذف آی دی کانال : '+inter(channel_id)+'","callback_data":"5"}],[{"text":"پیام خوش آمد گویی : '+inter(joinchat)+'","callback_data":"6"}],[{"text":"قفل فوروارد از افراد : '+inter(forward_id)+'","callback_data":"7"}]]}'
                if notAdmin(chat_id, user_id)==True:
                  if "forward_from" in updates["result"][i]["message"] and forward_id==True:
                    delete_message(message_id, chat_id)
                  if "forward_from_chat" in updates["result"][i]["message"] and forward_channel==True:
                    delete_message(message_id, chat_id)
                  if "entities" in updates["result"][i]["message"]:
                    entnum=len(updates["result"][i]["message"]["entities"])
                    for j in list(range(0, entnum)):
                      offset=updates["result"][i]["message"]["entities"][j-1]["offset"]
                      length=updates["result"][i]["message"]["entities"][j-1]["length"]
                      if updates["result"][i]["message"]["entities"][j-1]["type"]=="url" and link==True:
                        delete_message(message_id, chat_id)
                      if updates["result"][i]["message"]["entities"][j-1]["type"]=="mention" and channel_id==True and isChannel(updates["result"][i]["message"]["text"], offset, length)==True:              
                        delete_message(message_id, chat_id)
                  if "new_chat_member" in updates["result"][i]["message"]:
                    userid=updates["result"][i]["message"]["new_chat_member"]["id"]
                    isbot=updates["result"][i]["message"]["new_chat_member"]["is_bot"]
                    if isbot==True and bot==True:
                      ban_user(chat_id, userid)
                    else:
                      first_name=updates["result"][i]["message"]["new_chat_member"]["first_name"]
                      if "last_name" in updates["result"][i]["message"]["new_chat_member"]:
                        last_name=updates["result"][i]["message"]["new_chat_member"]["last_name"]
                      else:
                        last_name=""
                      group_name_2=group_name.replace("&", "%26")
                      first_name_2=first_name.replace("&", "%26")
                      last_name_2=last_name.replace("&", "%26")
                      send_message(jointext.format(first_name_2 ,last_name_2 , group_name_2), chat_id)
                if notAdmin(chat_id, user_id)==False:
                  if "text" in updates["result"][i]["message"]:
                    text=updates["result"][i]["message"]["text"]
                    if "reply_to_message" in updates["result"][i]["message"]:
                      reply_message_id=updates["result"][i]["message"]["reply_to_message"]["message_id"]
                      reply_user_id=updates["result"][i]["message"]["reply_to_message"]["from"]["id"]
                      if text=="سنجاق":
                        pin_message(chat_id, reply_message_id)     
                      if text=="بن":
                        ban_user(chat_id, reply_user_id)
                        send_message("کاربر با موفقیت بن شد", chat_id)
                      if text=="ساکت":
                        silent_user(chat_id, reply_user_id)
                        send_message("کاربر با موفقیت ساکت شد", chat_id)
                      if text=="آزاد کردن" or text=="ازاد کردن":
                        free_user(chat_id, reply_user_id)
                        send_message("کاربر با موفقیت آزاد شد", chat_id)
                      if text=="حذف پیام":
                        delete_message(message_id, chat_id)
                        delete_message(reply_message_id, chat_id)
                    if text=="تنظیمات":
                      url = URL + 'sendMessage?text=برای تنظیم ربات از کلید های زیر استفاده کنید&' + inline_keyboard
                      get_url(url)
                    if text=="راهنما":
                      send_message("""🗒دستورات ربات :
~~~~~~~~~~~~~~~
🔵بن 
🔺به صورت reply به پیام شخصی که میخواید از گروه حذف و بن بشه 
~~~~~~~~~~~~~~~
🔵ساکت 
🔺به صورت reply به پیام شخصی که میخواید به حالت سکوت بره و نتونه پیام بده
~~~~~~~~~~~~~~~
🔵آزاد کردن 
🔺به صورت reply به پیام شخصی که میخواید تمام محدودیت های اون برداشته بشه (بن و سکوت)
~~~~~~~~~~~~~~~
🔵تنظیمات
🔺وقتی این دستور رو بزنید یک کیبورد شیشه ای براتون باز میشه که میتونید با اون قفل پیام ها رو فعال و غیر فعال کنید""", chat_id)
    
              else:
                send_message("با سلام گروه شما در این ربات ثبت نشده است برای ثبت گروه خود با یکی از دو آی دی زیر هماهنگ کنید:\n@arsalan_geek \n@arsalan_darvishi",chat_id)
              if user_id==bot_admin :
                  if "text" in updates["result"][i]["message"]:
                      text=updates["result"][i]["message"]["text"]
                      if text=="add group":
                        add_group(chat_id)
                        send_message("گروه با موفقیت اضافه شد", chat_id)
                      if text=="ping":
                        send_message("pong😁", chat_id)
                        print("ping")
          else:
            print("message not difined!")
            print("\n\n")
            print(updates)
            print("\n\n")             
