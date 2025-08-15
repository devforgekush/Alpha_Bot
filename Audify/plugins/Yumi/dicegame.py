# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from pyrogram import Client, enums, filters
import asyncio
from Audify import app as app
from pyrogram.handlers import MessageHandler


@app.on_message(filters.command("dice"))
async def dice(bot, message):
    x = await bot.send_dice(message.chat.id)
    m = x.dice.value
    await message.reply_text(f"🎲 Hey {message.from_user.mention}, your score is: `{m}`", quote=True)


@app.on_message(filters.command("dart"))
async def dart(bot, message):
    x = await bot.send_dice(message.chat.id, "🎯")
    m = x.dice.value
    await message.reply_text(f"🎯 Hey {message.from_user.mention}, your score is: `{m}`", quote=True)


@app.on_message(filters.command("basket"))
async def basket(bot, message):
    x = await bot.send_dice(message.chat.id, "🏀")
    m = x.dice.value
    await message.reply_text(f"🏀 Hey {message.from_user.mention}, your score is: `{m}`", quote=True)


@app.on_message(filters.command(["jackpot", "slot"]))
async def jackpot(bot, message):
    x = await bot.send_dice(message.chat.id, "🎰")
    m = x.dice.value
    await message.reply_text(f"🎰 Hey {message.from_user.mention}, your score is: `{m}`", quote=True)


@app.on_message(filters.command(["ball", "bowling"]))
async def ball(bot, message):
    x = await bot.send_dice(message.chat.id, "🎳")
    m = x.dice.value
    await message.reply_text(f"🎳 Hey {message.from_user.mention}, your score is: `{m}`", quote=True)


@app.on_message(filters.command("football"))
async def football(bot, message):
    x = await bot.send_dice(message.chat.id, "⚽")
    m = x.dice.value
    await message.reply_text(f"⚽ Hey {message.from_user.mention}, your score is: `{m}`", quote=True)


@app.on_message(filters.command("toss"))
async def toss(bot, message):
    result = "Heads 🪙" if bool(asyncio.get_event_loop().time() % 2 < 1) else "Tails 🪙"
    await message.reply_text(f"🪙 Coin Toss Result: `{result}`", quote=True)


@app.on_message(filters.command("roll"))
async def roll(bot, message):
    from random import randint
    result = randint(1, 6)
    await message.reply_text(f"🎲 You rolled a `{result}`!", quote=True)


__help__ = """
🎮 **Play Game with Fun Emojis**

• `/dice` - Roll a dice 🎲  
• `/dart` - Throw a dart 🎯  
• `/basket` - Shoot a basketball 🏀  
• `/ball` or `/bowling` - Bowl a ball 🎳  
• `/football` - Kick a football ⚽  
• `/jackpot` or `/slot` - Spin the slot machine 🎰  
• `/toss` - Toss a coin 🪙  
• `/roll` - Roll a dice manually 🎲  
"""

__mod_name__ = "Games"
