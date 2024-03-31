# setup
from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import Application , CommandHandler , MessageHandler , filters , ContextTypes
import json
from datetime import datetime

#commands

async def start_command(update:Update , context:ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text("""pitikoo pitikoo
well Hello there I am pitikoo""")

async def help_command(update:Update , context:ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text("just pitikoo pitikoo")

async def custom_command(update:Update , context:ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text("custom cammand")

async def remain_command(update:Update , context:ContextTypes.DEFAULT_TYPE):
  await update.message.reply_text("""
برای بدست اوردن باقی مانده دو عددبرای مثال 8 بر 2 به صورت زیر پیامتان را وارد کنید
باقی مانده 8 2""")

# Rresponses

def handle_responses(text) -> str:
  text = text.lower()

  if 'hello' in text:
    return "pitikoo pitikoo  Hello  Pitikoo pitikoo"

  elif 'pitikoo' in text:
    return "ha ha funy"

  elif ("باقی مانده" in text) or ("باقیمانده" in text):
    text = text.replace("باقی مانده" , "").replace("باقیمانده" , "")
    print(text , "\n\n")
    num1, num2 = map(float, text.split())
    print(num1 ," ", num2)
    return str(num1 % num2)

  else:
    return 'just pitkoo pitikoo'

async def handle_message(update:Update , context:ContextTypes.DEFAULT_TYPE):

  username = update.message.from_user.username
  user_id = str(update.message.chat.id)
  text = update.message.text
  message_type = update.message.chat.type
  first_name = update.message.from_user.first_name
  print(first_name)

  if message_type == 'private':

    with open('user_messages.json' , 'r') as json_file:
      try:
        user_messages = json.load(json_file)
      except:
        user_messages = {}

    print("user_messages" , user_messages , "\n")

    if user_id not in list(user_messages.keys()):
      print("new user added", '\n')
      user_messages[user_id] = {}
      user_messages[user_id]['info'] = {'first_name':first_name,'username':username}
      user_messages[user_id]['messages'] = []

    user_messages[user_id]['messages'].append({'message': text  , 'time' :str(datetime.now())})
    with open('user_messages.json', 'w') as json_file:
          json.dump(user_messages, json_file, indent=4)

  print(f'User ({update.message.chat.id}) in {message_type} : "{text}"')

  if message_type == 'group':
    if os.getenv('BOT_USERNAME') in text:
      new_text = text.replace(os.getenv('BOT_USERNAME') , '').strip()
      respons = handle_responses(new_text)

    else:
      return

  else:
    respons = handle_responses(text)

  print('Bot:' , respons)                   # for debugging
  await update.message.reply_text(respons)



async def error(update:Update , context:ContextTypes.DEFAULT_TYPE):
  print(f'Update {update} caused error {context.error}')



if __name__ == '__main__':
  load_dotenv()
  print("starting bot ...")
  app = Application.builder().token(os.getenv('TOKEN')).build()

  #commands
  app.add_handler(CommandHandler('start' , start_command))
  app.add_handler(CommandHandler('help' , help_command))
  app.add_handler(CommandHandler('custom' , custom_command))
  app.add_handler(CommandHandler("remain" , remain_command))

  # Messsages
  app.add_handler(MessageHandler(filters.TEXT , handle_message))

  # Errors
  app.add_error_handler(error)

  
  # polls the bot
  print('polling ...')
  app.run_polling(poll_interval=3)

