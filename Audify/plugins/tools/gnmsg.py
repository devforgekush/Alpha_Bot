import re
import random
from pyrogram import filters
from Audify import app

# ✅ Good Night Handler
@app.on_message(
    filters.text & filters.regex(r"(?i)\b(good\s?night|gn|night|sleep\s?time)\b")
    | filters.command(["gn", "goodnight", "night", "sleep", "n"])
)
async def goodnight_command_handler(_, message):
    user = message.from_user.mention
    emoji = get_random_night_emoji()
    text = get_random_night_message(user).replace("😴", emoji)
    await message.reply_text(text)


def get_random_night_emoji():
    emojis = [
        "😴", "💤", "😪", "🌙", "🛌", "✨", "🕯️", "🌌", "🥱", "🛏️"
    ]
    return random.choice(emojis)


def get_random_night_message(user):
    messages = [
        f"Good night, {user}. 😴 May your dreams be filled with peace and happiness.",
        f"{user}, time to relax and drift into a deep sleep. 😴",
        f"Sweet dreams, {user}. 😴 Sleep well and rest easy tonight.",
        f"{user}, may the stars guide you into a peaceful slumber. 😴",
        f"Nighty night, {user}! 😴 Hope tomorrow brings you joy.",
        f"{user}, let the darkness of the night heal your soul. 😴",
        f"Lights out, {user}. 😴 Rest your mind and body now.",
        f"Have a peaceful night, {user}. 😴 Dream big and sleep tight.",
        f"{user}, it's bedtime! 😴 Recharge for a beautiful tomorrow.",
        f"{user}, wrap yourself in a cozy blanket and enter dreamland. 😴",
        f"{user}, stars are shining just for you tonight. 😴",
        f"Close your eyes and drift off, {user}. 😴",
        f"Let go of today, {user}. 😴 Embrace the calm of night.",
        f"{user}, may your night be filled with beautiful dreams. 😴",
        f"Sleep tight, {user}. 😴 You are safe and loved.",
        f"{user}, good night! 😴 Let your heart rest too.",
        f"{user}, surrender to sleep. 😴 You’ve earned it.",
        f"{user}, dream without fear. 😴 Sleep without worry.",
        f"Good night, {user}. 😴 You’ve done enough for today.",
        f"{user}, may tomorrow be kind to you. 😴 Rest well tonight.",
        f"{user}, peace be with you as you sleep. 😴",
        f"{user}, pillow hugs and dream kisses await. 😴",
        f"{user}, you've done well. 😴 Now drift away.",
        f"{user}, your soul needs rest too. 😴",
        f"{user}, see you in dreamland. 😴",
        f"{user}, the night whispers calmness to you. 😴",
        f"Sleep peacefully, {user}. 😴 You're amazing.",
        f"{user}, even the moon watches over you tonight. 😴",
        f"{user}, you made it through the day. 😴",
        f"Rest well, {user}. 😴 Tomorrow is full of possibilities.",
        f"Let go, {user}. 😴 Everything else can wait till morning.",
        f"{user}, no thoughts now. 😴 Only dreams.",
        f"{user}, you deserve soft dreams and a calm heart. 😴",
        f"{user}, you're not alone. 😴 The night hugs you gently.",
        f"{user}, you’ve been strong all day. 😴 Time to rest.",
        f"{user}, no alarms now. 😴 Just sweet dreams ahead.",
        f"{user}, drift into peace. 😴 You are enough.",
        f"{user}, everything will be okay. 😴 Sleep well.",
        f"{user}, let the stars carry your stress away. 😴",
        f"{user}, rest is the best self-care. 😴 Do it right.",
        f"{user}, tonight is your reset. 😴 Take it slow.",
        f"{user}, your dreams matter too. 😴 Don't hold back.",
        f"{user}, the night sky glows for you. 😴",
        f"{user}, your heart beats calm tonight. 😴",
        f"{user}, slow breaths, deep peace. 😴 Now sleep.",
        f"{user}, you did your best today. 😴 Be proud and rest.",
        f"{user}, time to drift gently into the night. 😴",
        f"{user}, the universe is quiet now. 😴 Join it.",
        f"{user}, healing begins with sleep. 😴 Let it come.",
        f"{user}, you're loved more than you know. 😴",
        f"{user}, sleep without fear. 😴 You're safe here.",
        f"{user}, the moonlight covers you with comfort. 😴"
    ]
    return random.choice(messages)


# ✅ Good Morning Handler
@app.on_message(
    filters.text & filters.regex(r"(?i)\b(good\s?morning|gm|morning|morning\s?time)\b")
    | filters.command(["gm", "goodmorning", "morning", "m"])
)
async def goodmorning_command_handler(_, message):
    user = message.from_user.mention
    emoji = get_random_morning_emoji()
    text = get_random_morning_message(user).replace("🌞", emoji)
    await message.reply_text(text)


def get_random_morning_emoji():
    emojis = [
        "🌞", "🌅", "☀️", "🌄", "🍃", "🕊️", "🌻", "🫧", "✨", "🌸"
    ]
    return random.choice(emojis)


def get_random_morning_message(user):
    messages = [
        f"Good morning, {user}! 🌞 Wishing you a peaceful and productive day ahead.",
        f"{user}, may your morning be as bright and beautiful as your smile. 🌞",
        f"Rise and shine, {user}! 🌞 Let today be full of positivity.",
        f"{user}, sending morning sunshine and lots of energy your way! 🌞",
        f"Hello, {user}! 🌞 Wake up and embrace the magic of today.",
        f"🌞 A new day has begun, {user}. Fill it with joy and purpose.",
        f"{user}, good morning! 🌞 Make this day your masterpiece.",
        f"Let every sunrise bring you hope, {user}. 🌞 Have a fresh start!",
        f"{user}, today is a blank page—write a wonderful story. 🌞",
        f"{user}, awaken your spirit. 🌞 The world awaits your light.",
        f"{user}, welcome the day with a smile. 🌞 You’ve got this!",
        f"{user}, the morning sun brings endless possibilities. 🌞",
        f"Start strong, stay positive, {user}. 🌞 Good morning!",
        f"{user}, may your coffee be strong and your day be sweet. 🌞",
        f"{user}, morning vibes and fresh motivation coming your way! 🌞",
        f"{user}, let gratitude fill your morning. 🌞 Life is beautiful.",
        f"🌞 Good morning, {user}. Take a deep breath and shine!",
        f"{user}, this morning is a gift—unwrap it with joy! 🌞",
        f"{user}, may your day be filled with little wins and big smiles. 🌞",
        f"New day, new energy, {user}. 🌞 Let's go win it!",
        f"{user}, it’s time to rise and sparkle. 🌞",
        f"{user}, believe in yourself and enjoy this fresh start. 🌞",
        f"{user}, mornings are for motivation and miracles. 🌞",
        f"{user}, you’ve got a full day to bloom. 🌞 Let’s make it count.",
        f"{user}, start today with courage, peace, and determination. 🌞",
        f"{user}, open your eyes to the joy today brings. 🌞",
        f"🌞 Sending light, love, and peace your way, {user}.",
        f"Good morning to the amazing {user}. 🌞 Go out and shine!",
        f"{user}, every morning brings a chance to grow. 🌞",
        f"{user}, a smile is the best accessory this morning. 🌞 Wear it well.",
        f"{user}, you are powerful, smart, and ready to win the day. 🌞"
    ]
    return random.choice(messages)
