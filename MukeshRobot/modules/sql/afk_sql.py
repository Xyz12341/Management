import threading
from sqlalchemy import BigInteger, Boolean, Column, UnicodeText
from MukeshRobot.modules.sql import BASE, SESSION
from pyrogram import Client, filters
from pyrogram.enums import ChatType

# Replace this with the actual GIF URL you want to use
afk_gif_url = "https://media.giphy.com/media/VbnUQpnihPSIgIXuZv/giphy.gif"


class AFK(BASE):
    __tablename__ = "afk_users"

    user_id = Column(BigInteger, primary_key=True)
    is_afk = Column(Boolean)
    reason = Column(UnicodeText)

    def __init__(self, user_id, reason="", is_afk=True):
        self.user_id = user_id
        self.reason = reason
        self.is_afk = is_afk

    def __repr__(self):
        return "afk_status for {}".format(self.user_id)


AFK.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()

AFK_USERS = {}


# Function to check if a user is AFK
def is_afk(user_id):
    return user_id in AFK_USERS


# Function to check AFK status from SQL
def check_afk_status(user_id):
    try:
        return SESSION.query(AFK).get(user_id)
    finally:
        SESSION.close()


# Function to set AFK status
def set_afk(user_id, reason=""):
    with INSERTION_LOCK:
        curr = SESSION.query(AFK).get(user_id)
        if not curr:
            curr = AFK(user_id, reason, True)
        else:
            curr.is_afk = True

        AFK_USERS[user_id] = reason

        SESSION.add(curr)
        SESSION.commit()


# Function to remove AFK status
def rm_afk(user_id):
    with INSERTION_LOCK:
        curr = SESSION.query(AFK).get(user_id)
        if curr:
            if user_id in AFK_USERS:  # sanity check
                del AFK_USERS[user_id]

            SESSION.delete(curr)
            SESSION.commit()
            return True

        SESSION.close()
        return False


# Function to toggle AFK status
def toggle_afk(user_id, reason=""):
    with INSERTION_LOCK:
        curr = SESSION.query(AFK).get(user_id)
        if not curr:
            curr = AFK(user_id, reason, True)
        elif curr.is_afk:
            curr.is_afk = False
        else:
            curr.is_afk = True
        SESSION.add(curr)
        SESSION.commit()


# Load AFK users from the database
def __load_afk_users():
    global AFK_USERS
    try:
        all_afk = SESSION.query(AFK).all()
        AFK_USERS = {user.user_id: user.reason for user in all_afk if user.is_afk}
    finally:
        SESSION.close()


__load_afk_users()


# AFK command handler
@Client.on_message(filters.command("afk"))
async def afk_command_handler(client, message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if message.chat.type != ChatType.PRIVATE:
        if len(message.command) > 1:
            reason = " ".join(message.command[1:])
        else:
            reason = "No reason provided."

        # Set AFK status and send a message with the GIF
        set_afk(user_id, reason)

        afk_message = f"**User is now AFK**\nReason: {reason}"
        await client.send_animation(chat_id, afk_gif_url, caption=afk_message)
    else:
        await message.reply_text("This command can only be used in groups.")


# Command to remove AFK
@Client.on_message(filters.command("back"))
async def back_command_handler(client, message):
    user_id = message.from_user.id

    # Remove AFK status
    if rm_afk(user_id):
        await message.reply_text("Welcome back! You're no longer AFK.")
    else:
        await message.reply_text("You were not AFK.")
