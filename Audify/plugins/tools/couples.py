import random
from datetime import datetime
from pyrogram import *
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from Audify import app
from config import SUPPORT_CHAT

# Inline buttons: Support and Close only
POLICE = InlineKeyboardMarkup([
    [InlineKeyboardButton("💬 Support", url=SUPPORT_CHAT)],
    [InlineKeyboardButton("✖️ Close", callback_data="close")]
])

# Date utils
def dt():
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M")
    return dt_string.split(" ")

def dt_tom():
    return (
        str(int(dt()[0].split("/")[0]) + 1)
        + "/" + dt()[0].split("/")[1]
        + "/" + dt()[0].split("/")[2]
    )

tomorrow = str(dt_tom())
today = str(dt()[0])

# Couple command
@app.on_message(filters.command("couples"))
async def ctest(_, message):
    cid = message.chat.id
    if message.chat.type == ChatType.PRIVATE:
        return await message.reply_text("⚠️ This command works only in groups.")
    try:
        msg = await message.reply_text("💞")
        list_of_users = []

        async for i in app.get_chat_members(cid, limit=50):
            if not i.user.is_bot:
                list_of_users.append(i.user.id)

        c1_id = random.choice(list_of_users)
        c2_id = random.choice(list_of_users)
        while c1_id == c2_id:
            c1_id = random.choice(list_of_users)

        N1 = (await app.get_users(c1_id)).mention
        N2 = (await app.get_users(c2_id)).mention

        TXT = f"""
💖 Couple of the Day 💖

{N1} + {N2} = ❤️

📅 Next couple will be selected on:
➤ {tomorrow}
"""
        await message.reply_text(TXT.strip(), reply_markup=POLICE)
        await msg.delete()

    except Exception as e:
    from Audify.logger import LOGGER
    LOGGER(__name__).error(str(e))

# Help section
__mod__ = "Couples"
__help__ = """
/couples - Show the couple of the day in the group 💞
"""
