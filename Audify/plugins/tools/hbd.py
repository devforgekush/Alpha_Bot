# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import random
from pyrogram import filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from Audify import app

# 🎯 Birthday triggers (case-insensitive)
BIRTHDAY_COMMANDS = [
    "hbd", "Hbd", "HBD", "bdy", "BDY", "Bdy",
    "appy", "Birthday", "birthday", "appy birthday", "ppy bdy"
]

# 🎉 Emoji list
BIRTHDAY_EMOJIS = [
    "🎉", "🎂", "🎈", "🎊", "🥳", "🍰", "🪩", "🍬", "🍾", "🎁"
]

# 🎊 Birthday replies
BIRTHDAY_REPLIES = [
    "Happy Birthday! Wishing you a day full of joy and laughter.",
    "Many happy returns of the day!",
    "May all your dreams come true this year.",
    "Celebrate big, smile bigger!",
    "Sending you the biggest slice of happiness today!",
    "Hope your birthday is as special as you are.",
    "Another year wiser. Happy Birthday!",
    "Time to unwrap joy. Happy Birthday!",
    "Party hard, but don’t forget the cake!",
    "Cheers to you and your wonderful life ahead!",
    "Make a wish and blow the candles!",
    "Today is your day. Shine bright!",
    "Birthdays are nature’s way of telling us to eat more cake.",
    "Have a sweet and fabulous birthday!",
    "Keep calm and celebrate your day!",
    "Birthdays look good on you!",
    "Wishing you a year full of blessings.",
    "Hope today fills your heart with joy!",
    "You deserve all the good things today.",
    "Today is a celebration of YOU!",
    "Let’s celebrate your existence!",
    "May this year bring success your way.",
    "Live, laugh, party. Happy Birthday!",
    "Stay awesome and keep smiling.",
    "It’s not the years, it’s the memories.",
    "Time to level up in life!",
    "You’re one of a kind. Enjoy your day!",
    "Your special day deserves special vibes.",
    "Smile big today and every day.",
    "Count your blessings, not your candles!",
    "Life gave us you—best gift ever!",
    "Let the birthday magic begin!",
    "Aging like fine wine!",
    "Keep glowing and growing.",
    "You make the world brighter. Happy Birthday!",
    "A legend was born today!",
    "Cake, gifts, and laughter await!",
    "Birthdays are meant for fun. Go wild!",
    "A toast to your journey ahead!",
    "Time to celebrate YOU!",
    "Sending good vibes your way.",
    "Make this day unforgettable.",
    "You’ve unlocked a new year!",
    "Let’s make memories today.",
    "May your day be filled with joy.",
    "A day just for you. Enjoy it!",
    "You’re worth every celebration!",
    "Let happiness be your gift today.",
    "Another chapter begins—make it great!",
    "You’ve earned all the smiles today!"
]

# ⏹ Inline Close Button
CLOSE_BUTTON = InlineKeyboardMarkup([
    [InlineKeyboardButton("⏹ Close", callback_data="close")]
])

# 🏷️ Get the mentioned or replied user
def tag_target_user(message: Message):
    if message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        user = message.from_user
    return user.mention if user else "Someone"

# 🎂 Prefixless birthday detector that doesn't block other handlers
@app.on_message(filters.group & filters.text, group=-1)
async def birthday_detector(_, message: Message):
    text = message.text.lower().strip()
    if any(text == cmd.lower() for cmd in BIRTHDAY_COMMANDS):
        target = tag_target_user(message)
        emoji = random.choice(BIRTHDAY_EMOJIS)
        wish = random.choice(BIRTHDAY_REPLIES)

        await message.reply_text(
            f"{emoji} <b>{wish}</b>\n\n— {target}",
            parse_mode=ParseMode.HTML,
            reply_markup=CLOSE_BUTTON
        )
