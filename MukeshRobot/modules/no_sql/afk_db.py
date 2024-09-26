from MukeshRobot.modules.no_sql import Mukeshdb
from pyrogram import Client, filters
from pyrogram.enums import ChatType

afkdb = Mukeshdb.afk

# Replace this with the actual GIF URL you want to use
afk_gif_url = "https://media.giphy.com/media/VbnUQpnihPSIgIXuZv/giphy.gif"


# Function to check if the user is AFK
async def is_afk(user_id: int) -> bool:
    user = await afkdb.find_one({"user_id": user_id})
    if not user:
        return False, {}
    return True, user["reason"]


# Function to add a user to the AFK list with a reason (or mode)
async def add_afk(client: Client, user_id: int, chat_id: int, mode: str):
    # Update or add user to AFK list in the database
    await afkdb.update_one(
        {"user_id": user_id}, {"$set": {"reason": mode}}, upsert=True
    )

    # Notify the group with AFK reason and a GIF
    afk_message = f"**User is now AFK**\nReason: {mode}"
    
    # Send the AFK GIF with the message
    await client.send_animation(chat_id, afk_gif_url, caption=afk_message)


# Function to remove the user from the AFK list
async def remove_afk(user_id: int):
    user = await afkdb.find_one({"user_id": user_id})
    if user:
        return await afkdb.delete_one({"user_id": user_id})


# Function to get a list of all AFK users
async def get_afk_users() -> list:
    users = afkdb.find({"user_id": {"$gt": 0}})
    if not users:
        return []
    users_list = []
    for user in await users.to_list(length=1000000000):
        users_list.append(user)
    return users_list


# AFK command handler for Pyrogram
@Client.on_message(filters.command("afk"))
async def afk_command_handler(client, message):
    user_id = message.from_user.id
    chat_id = message.chat.id

    if message.chat.type != ChatType.PRIVATE:
        if len(message.command) > 1:
            reason = " ".join(message.command[1:])
        else:
            reason = "No reason provided."

        # Add the user to AFK and send the message with the GIF
        await add_afk(client, user_id, chat_id, reason)

        await message.reply_text(f"You're now AFK!\nReason: {reason}")
    else:
        await message.reply_text("This command can only be used in groups.")


# Command to remove AFK (optional)
@Client.on_message(filters.command("back"))
async def back_command_handler(client, message):
    user_id = message.from_user.id

    # Remove the user from AFK list
    await remove_afk(user_id)

    await message.reply_text("Welcome back! You're no longer AFK.")
