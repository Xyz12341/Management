import html
import re
from telegram import (
    CallbackQuery,
    Chat,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ParseMode,
    Update,
    User,
)
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    CommandHandler,
    Filters,
    MessageHandler,
)
from telegram.utils.helpers import mention_html

import MukeshRobot.modules.sql.chatbot_sql as sql
from MukeshRobot import BOT_ID, BOT_USERNAME, dispatcher
from MukeshRobot.modules.helper_funcs.chat_status import user_admin, user_admin_no_reply
from MukeshAPI import api

@user_admin_no_reply
def mukeshrm(update: Update, context: CallbackContext) -> str:
    query = update.callback_query
    user = update.effective_user
    match = re.match(r"rm_chat(.+?)", query.data)
    if match:
        chat: Chat = update.effective_chat
        sql.set_mukesh(chat.id)
        return (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"Chatbot has been <b>disabled</b>.\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}"
        )

@user_admin_no_reply
def mukeshadd(update: Update, context: CallbackContext) -> str:
    query = update.callback_query
    user = update.effective_user
    match = re.match(r"add_chat(.+?)", query.data)
    if match:
        chat: Chat = update.effective_chat
        sql.rem_mukesh(chat.id)
        return (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"Chatbot has been <b>enabled</b>.\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}"
        )

@user_admin
def mukesh(update: Update, context: CallbackContext):
    message = update.effective_message
    msg = "Choose an option to enable/disable the chatbot:"
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="Enable", callback_data="add_chat({})"),
                InlineKeyboardButton(text="Disable", callback_data="rm_chat({})"),
            ]
        ]
    )
    message.reply_text(text=msg, reply_markup=keyboard, parse_mode=ParseMode.HTML)

def mukesh_message(context: CallbackContext, message):
    reply_message = message.reply_to_message
    if message.text.lower() == "mukesh":
        return True
    elif BOT_USERNAME in message.text.upper():
        return True
    elif reply_message and reply_message.from_user.id == BOT_ID:
        return True
    return False

def chatbot(update: Update, context: CallbackContext):
    message = update.effective_message
    chat_id = update.effective_chat.id
    bot = context.bot

    # Check if the chatbot is enabled in this chat
    if sql.is_mukesh(chat_id):
        return

    if message.text and not message.document:
        if not mukesh_message(context, message):
            return
        bot.send_chat_action(chat_id, action="typing")
        response = api.chatgpt(message.text, mode="gf")["results"]
        message.reply_text(response)

# Handlers
CHATBOTK_HANDLER = CommandHandler("chatbot", mukesh, run_async=True)
ADD_CHAT_HANDLER = CallbackQueryHandler(mukeshadd, pattern=r"add_chat", run_async=True)
RM_CHAT_HANDLER = CallbackQueryHandler(mukeshrm, pattern=r"rm_chat", run_async=True)
CHATBOT_HANDLER = MessageHandler(
    Filters.text
    & (~Filters.regex(r"^#[^\s]+") & ~Filters.regex(r"^!") & ~Filters.regex(r"^\/")),
    chatbot,
    run_async=True,
)

dispatcher.add_handler(ADD_CHAT_HANDLER)
dispatcher.add_handler(CHATBOTK_HANDLER)
dispatcher.add_handler(RM_CHAT_HANDLER)
dispatcher.add_handler(CHATBOT_HANDLER)

__handlers__ = [
    ADD_CHAT_HANDLER,
    CHATBOTK_HANDLER,
    RM_CHAT_HANDLER,
    CHATBOT_HANDLER,
]
