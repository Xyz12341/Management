import asyncio
from platform import python_version as pyver
from pyrogram.enums import ChatType
from pyrogram import __version__ as pver
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from telegram import __version__ as lver
from telethon import __version__ as tver
from MukeshRobot.modules.no_sql import add_served_chat,save_id
from MukeshRobot import SUPPORT_CHAT, pbot,BOT_USERNAME, OWNER_ID,BOT_NAME,START_IMG

async def member_permissions(chat_id: int, user_id: int):
    perms = []
    member = (await pbot.get_chat_member(chat_id, user_id)).privileges
    if not member:
        return []
    if member.can_post_messages:
        perms.append("can_post_messages")
    if member.can_edit_messages:
        perms.append("can_edit_messages")
    if member.can_delete_messages:
        perms.append("can_delete_messages")
    if member.can_restrict_members:
        perms.append("can_restrict_members")
    if member.can_promote_members:
        perms.append("can_promote_members")
    if member.can_change_info:
        perms.append("can_change_info")
    if member.can_invite_users:
        perms.append("can_invite_users")
    if member.can_pin_messages:
        perms.append("can_pin_messages")
    if member.can_manage_video_chats:
        perms.append("can_manage_video_chats")
    return perms

PHOTO = [
    "https://telegra.ph/file/e2e2b8f98caa698fa639d.jpg",
    "https://telegra.ph/file/2748bea032f761d7e19ef.jpg",
    "https://telegra.ph/file/99b11ca3d972fc46001db.jpg",
    "https://telegra.ph/file/541e75860e2126a153c18.jpg",
    "https://telegra.ph/file/2ac48eb1a970b615a0256.jpg",
]

Mukesh = [
    [
        InlineKeyboardButton(text="ᴜᴘᴅᴀᴛᴇ", url=f"https://t.me/kittyxupdates"),
        InlineKeyboardButton(text="ꜱᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"),
    ],
    [
        InlineKeyboardButton(
            text="˹🕸️ ᴛᴧᴘ тᴏ sᴇᴇ ᴍᴧɢɪᴄ 🕸️˼",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
]



@pbot.on_message(filters.command("alive"))
async def restart(client, m: Message):
    await m.delete()
    accha = await m.reply("🐬")
    await asyncio.sleep(0.2)
    await accha.edit("💤")

    await accha.delete()
    await asyncio.sleep(0.3)
    
    umm = await m.reply_sticker(
        "CAACAgUAAxkDAAJHbmLuy2NEfrfh6lZSohacEGrVjd5wAAIOBAACl42QVKnra4sdzC_uKQQ"
    )
    await umm.delete()
    owner=await pbot.get_users(OWNER_ID)
    await m.reply_photo(
        START_IMG,
        caption=f"""** ✦ ʜᴇʏ, ɪ ᴀᴍ [{BOT_NAME}](f"t.me/{BOT_USERNAME}") ✦**\n\n❍ **ʟɪʙʀᴀʀʏ ➛** `{lver}`\n❍ **ᴛᴇʟᴇᴛʜᴏɴ ➛** `{tver}`\n❍ **ᴘʏʀᴏɢʀᴀᴍ ➛** `{pver}`\n❍ **ᴘʏᴛʜᴏɴ ➛** `{pyver()}`\n\n❍ **ᴍᴀᴅᴇ ʙʏ ➛** [🇲σ᭡፝֟ɳ🌙](tg://user?id={OWNER_ID})""",
        reply_markup=InlineKeyboardMarkup(Mukesh)
    )

@pbot.on_message(group=1)
async def save_statss(_, m):
    try:
        if m.chat.type == ChatType.PRIVATE:
            save_id(m.from_user.id)
        elif m.chat.type==ChatType.SUPERGROUP:
            add_served_chat(m.chat.id)
        else:
            add_served_chat(m.chat.id)        

    except Exception as e:
        pass
       # await _.send_message(OWNER_ID,f"db error {e}")

__mod_name__ = "ᴀʟɪᴠᴇ"
__help__ = """
 ❍ /alive ➛ ᴄʜᴇᴄᴋ ʙᴏᴛ ᴀʟɪᴠᴇ sᴛᴀᴛᴜs.
 ❍ /ping ➛ ᴄʜᴋ ᴘɪɴɢ sᴛᴀᴛᴜs.
 ❍ /stats : sʜᴏᴡs ᴛʜᴇ ᴏᴠᴇʀᴀʟʟ sᴛᴀᴛs ᴏғ ᴛʜᴇ ʙᴏᴛ.

☆✧....𝐁𝐘🫧 » [☄️𝐌ᴏᴏɴ🌙](https://t.me/Moonshining2)....🥀🥀✧☆
 """

