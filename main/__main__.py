import logging
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, InlineQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext , Filters
import random
import json
from telegram.ext.dispatcher import run_async
import time
from main import dispatcher 
from telegram.ext import CommandHandler, InlineQueryHandler, \
    ConversationHandler  # conversation handler is like there are more than 1 step the bot needs to do , not just 1 question 1 answer , conversation handler is more complex to do
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, \
    ParseMode  # inline keyboard button is the button u saw earlier when i do the mypet , there are 3 buttons , and inline kyeboard markup is when u use it on the text  , parsemode is like HTML or MARKDOWN, to make text Bold , italic or underline
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext, \
    Filters  # callbackquery handler is when u in conversation handler and u want to callback to the button clicked by user to determine what is next steps, updater will fetch the data and pass to telegram so we need that for api keys
 
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
 
ONE, TWO, THREE, FOUR, FIRST, SECOND, *_ = range(50)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)
 
restaurant_list = []
 
def reset(update , context):
    restaurant_list.clear()
    update.message.reply_text('<b>the list has been successfully cleared</b>', parse_mode = ParseMode.HTML)
 
 
def restaurant(update, context):
    user = update.effective_user.name
    id = update.effective_user.id
    query = update.callback_query
    cd = context.chat_data
 
    keyboard = [
        [InlineKeyboardButton("0", callback_data= '0'),
         InlineKeyboardButton("1", callback_data='1'),
         InlineKeyboardButton("2", callback_data='2'),]
         ]
 
    reply_markup = InlineKeyboardMarkup(keyboard)
 
    update.message.reply_text(f'{user}, ????????????????????????????????????\n\n??????-  ???  0\n??????-  ???  1\n??????-  ???  2\n\n??????????????????', reply_markup=reply_markup)
    return ONE
 
 
def res0(update, context):
    query = update.callback_query
    cd = context.chat_data
 
    query.edit_message_text('??????????????????????????????')
    return ConversationHandler.END
 
 
def res1(update , context):
    query = update.callback_query
    cd = context.chat_data
 
    query.edit_message_text('Enter the name of restaurant to added into the list')
 
    return TWO
 
def res11(update, context):
    RL = restaurant_list
    try:
        choice = update.message.text
        restaurant_list.append(choice)
        context.bot.send_message(chat_id = update.effective_chat.id , text = f'You added {choice} into the list , the current list is now {RL}')
    except ValueError:
        context.bot.send_message('???????????????????????????')
 
    return restaurant(update, context)
 
 
def res2(update, context):
    RL = restaurant_list
    query = update.callback_query
    cd = context.chat_data
 
    result = random.choice(RL)
    context.bot.send_message(chat_id = update.effective_chat.id , text = f'List so far = {RL}\n\nRandom choice result = {result}\n\nThank you for using the service')
    return ConversationHandler.END
 
 
RES_HANDLER = ConversationHandler(
    entry_points=[CommandHandler('restaurant', restaurant)],
    states={
        ONE: [CallbackQueryHandler(res0, pattern='^0$'),
              CallbackQueryHandler(res1, pattern='^1$'),
              CallbackQueryHandler(res2, pattern='^2$'),
              ],
 
        TWO:[MessageHandler(Filters.text, res11)]
       },
    fallbacks=[],
    allow_reentry=True,
    per_user=True
    )
 
RESET_HANDLER = CommandHandler('reset', reset)
 
dispatcher.add_handler(RES_HANDLER)
dispatcher.add_handler(RESET_HANDLER)
 
