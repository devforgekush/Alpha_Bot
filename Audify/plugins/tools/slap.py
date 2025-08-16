import requests
from pyrogram import filters
from pyrogram.types import Message
from Audify import app

API_URL = "https://api.waifu.pics"

# ✅ SFW Action Categories with emojis
sfw_actions = {
    "waifu": "🌸", "neko": "🐱", "shinobu": "🍵", "megumin": "✨", "bully": "😈",
    "cuddle": "🤗", "cry": "😢", "hug": "🫂", "awoo": "🐺", "kiss": "😘",
    "lick": "👅", "pat": "🖐", "smug": "😏", "bonk": "🔨", "yeet": "📤",
    "blush": "😊", "smile": "😄", "wave": "👋", "highfive": "✋", "handhold": "🤝",
    "nom": "🍽", "bite": "😬", "glomp": "🫶", "slap": "😤", "kill": "💀",
    "kick": "🥾", "happy": "😁", "wink": "😉", "poke": "👉", "dance": "💃",
    "cringe": "😬"
}

# ✅ NSFW Action Categories with emojis
nsfw_actions = {
    "waifu": "🌸", "neko": "🐱", "trap": "👧", "blowjob": "😶‍🌫️"
}


# ✅ Helper to send image with proper await
async def send_action_image(client, message: Message, action_type: str, category: str, emoji: str):
    try:
        response = requests.get(f"{API_URL}/{action_type}/{category}")
        if response.status_code == 200:
            image_url = response.json().get("url")
            if not image_url:
                raise Exception("No image URL in response.")

            user = message.from_user
            sender_name = f"[{user.first_name}](tg://user?id={user.id})"

            if message.reply_to_message:
                replied_user = message.reply_to_message.from_user
                replied_name = f"[{replied_user.first_name}](tg://user?id={replied_user.id})"
                caption = f"{sender_name} sent **{category}** to {replied_name} {emoji}"
            else:
                caption = f"{sender_name} is feeling **{category}** {emoji}"

            await client.send_animation(
                chat_id=message.chat.id,
                animation=image_url,
                caption=caption,
                parse_mode="markdown"
            )
        else:
            await message.reply_text("❌ Error occurred while fetching image.")
    except Exception as e:
    from Audify.logger import LOGGER
    LOGGER(__name__).error(f"[Waifu.pics] Error: {e}")
        await message.reply_text("❌ Failed to get image from API.")


# ✅ Register SFW handlers
for category, emoji in sfw_actions.items():
    @app.on_message(filters.command(category))
    async def sfw_handler(client, message, category=category, emoji=emoji):
        await send_action_image(client, message, "sfw", category, emoji)


# ✅ Register NSFW handlers
for category, emoji in nsfw_actions.items():
    @app.on_message(filters.command(category))
    async def nsfw_handler(client, message, category=category, emoji=emoji):
        await send_action_image(client, message, "nsfw", category, emoji)
