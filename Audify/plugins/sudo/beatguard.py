# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import random
from pyrogram import filters
from pyrogram.types import ChatPermissions, ChatPrivileges, Message
from Audify import app
from Audify.misc import SUDOERS
from Audify.utils.Audify_BAN import admin_filter

# ❖ Default Replies for No Action
random_responses = [
    "Hey, why you disturbing me right now?",
    "Tum ho kaun pehle ye batao 😒",
    "Apne aap ko mere Owner samjhe ho kya?",
    "Main busy hoon, baad mein aana.",
    "Yeh kya naam le rahe ho mera, sone do mujhe 😴",
    "Haan bolo kya chahiye? Jaldi batao.",
    "Chup baitho! Time nahi hai tumhare liye.",
    "I'm currently unavailable. Try again never.",
    "Zyada baat mat karo warna block kar dungi 😒",
    "Are you serious? Mujhe peace chahiye!",
    "Talk to the hand ✋",
    "Aree kya musibat hai yaar 🥲",
    "Oye ja na, mujhe kuch kaam hai!",
    "Tumse pichhle janam ka badla lena hai kya mujhe?",
    "Ghar jao beta homework karo 📚",
    "Nikal pehli fursat mein 🚪",
    "Shanti rakho, Buddha mil gaya",
    "Suno, zindagi bohot choti hai — mujhe disturb na karo.",
    "Mood off hai, tumse baat nahi karni 😶",
    "Why are you so obsessed with me? 🙄",
    "Kya aapko bhi lagta hai mai cute hu?",
    "Tumhara time aayega... abhi jao!",
    "Apni aukaat mein raho, Audify hoon main.",
    "Chalo chalo line mein lago.",
    "Rehne do, tumse naa ho paayega.",
    "Tere jaise 12 dekhe hain maine!",
    "Bas kar pagle rulayega kya 😭",
    "Aur bhai kya haal chaal? (jk I don't care)",
    "Bore mat karo bro!",
    "Self destructing in 3...2...1 💣",
    "Chup baith! Admin bulao 😡",
    "Control Uday! Control 😤",
    "Baat karne ka mann nahi hai.",
    "Life mein peace chahiye bas.",
    "Main pagal hoon... aap kaun ho?",
    "Kal milte hain dream mein!",
    "Mat karo na bhai request... thak gaya hu.",
    "Bohot hard be! Audify mode ON 😎",
    "Suno... khud se baat karo... main nahi!",
    "Akele akele kya soche... chalo mute ho jao.",
    "Main tujhe restrict kar dungi 🛑",
    "Zyada shana mat ban!",
    "Beta tumse na ho payega!",
    "O bhai maro mujhe 😵",
    "Lauta do mere 2 minute 🕒",
    "Bro seriously? Yeh bhi ek request thi?",
    "Kabhi kabhi lagta hai apun hi bhagwan hai 🕉️",
    "Chill kar yaar!",
    "Audify hoon, bakchodi band!",
]

# ❖ If SUDO user is targeted
sudo_protect_texts = [
    "I can't restrict my boss! 😤",
    "This user pays my hosting bills, sorry not sorry.",
    "Admin toh admin hota hai, samjha karo!",
    "I’m loyal to my SUDO. Unlike you 🙄",
    "Don't touch my dev. He’ll uninstall me 😱",
    "Arey bhai! Uske haath mein meri jaan hai 💀",
    "Tumhare jaise 100 aaye, par SUDO ek hi hai 🔱",
    "Owner banne ka sapna dekhna band karo 😹",
    "Haha! You can't ban the king 👑",
    "This is not your level, beta.",
    "Bheek mang le, par SUDO pe hath mat daal 😂",
    "He can rewrite my code with one command, careful! 🧠",
    "Jab tak suraj chand rahega, SUDO amar rahega ☀️🌙",
    "Owner ko restrict karega? Soch bhi kaise liya! 🤡",
    "Nazar utarwa lo tumhari 🔮",
    "That’s like trying to slap God… in His own temple 🛕",
    "Beta tumse na ho payega 🥱",
    "SUDO is protected by divine firewall ⚡",
    "Kuch bhi! Ab Owner bhi ban hoga kya? 😭",
    "BSDK usi ne banaya mujhe 🤖",
    "Apni aukaat mein reh 🧍‍♂️",
    "This person is the reason I exist, bro. Show some respect.",
    "Haha good joke. Banning my creator? Dream on 💭",
    "Mere creator ke against command? Nice try, loser! 🤡",
    "Kar le jo karna hai, SUDO nahi jaayega 😎",
    "Owner deserves nothing but royal treatment 👑",
    "Bhagwan ko block karega kya? 🤣",
    "Error 403: You can’t mess with the boss",
    "Only God can judge SUDO. Not you!",
    "Tum jaise 4 aaye, ek Owner nahi mile 😌",
    "SUDO ke against command? Lemme just… ignore that 🗑️",
    "Tera dimag theek hai kya? 🤯",
    "SUDO tries to ban you, not the other way around 💣",
    "Back off! You're in a danger zone 🚫",
    "SUDO has ‘Do Not Disturb’ written all over him!",
    "Imagine trying to ban admin. Couldn’t be me 🙃",
    "Likh ke le le – Owner ban nahi hota 🤐",
    "Even your ancestors won’t dare that 😆",
    "Sharam aani chahiye 😒",
    "Bro, even I have limits 💀",
    "SUDO = untouchable ✋",
    "Mera malik hai woh, samjha karo ❤️",
    "Owner = infinity privileges. You = nada.",
    "SUDO is whitelisted in my heart ❤️",
    "He writes my code, I obey 🛐",
    "SUDO is my overlord. I shall obey.",
    "Kaan pakad le, aur maafi maang 😬",
    "Don't mess with karma, bro 😏",
    "Apne baap ko ban karega? 😂",
    "You dare oppose the one true coder?",
    "Bhai bhai bhai, jaan leni hai kya mujhe?"
]


# ❖ Command keywords
ban_words = ["ban", "boom"]
unban_words = ["unban"]
mute_words = ["mute", "silent", "shut"]
unmute_words = ["unmute", "speak", "free"]
kick_words = ["kick", "out", "nikaal", "nikal"]
promote_words = ["promote", "adminship"]
fullpromote_words = ["fullpromote", "fulladmin"]
demote_words = ["demote", "lelo"]

# ❖ Usage Help Text
usage_text = """
<b>🔧 Audify Admin Command Usage:</b>

Reply to a user's message and use any of the following:
• <code>/Audify ban</code> – Ban the user
• <code>/Audify unban</code> – Unban the user
• <code>/Audify mute</code> – Mute the user
• <code>/Audify unmute</code> – Unmute the user
• <code>/Audify kick</code> – Kick the user
• <code>/Audify promote</code> – Promote with limited rights
• <code>/Audify fullpromote</code> – Full admin rights
• <code>/Audify demote</code> – Remove admin rights

<i>⚠️ You must reply to a user's message.</i>
"""

# ❖ Audify Main Handler
@app.on_message(filters.command(["Audify"], prefixes=["/"]) & admin_filter)
async def Audify_cmd(_, message: Message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    args = message.text.split(maxsplit=1)

    if not reply:
        return await message.reply_text(usage_text)

    user_id = reply.from_user.id
    command = args[1].lower() if len(args) > 1 else ""

    for word in ban_words:
        if word in command:
            if user_id in SUDOERS:
                return await message.reply(random.choice(sudo_protect_texts))
            await _.ban_chat_member(chat_id, user_id)
            return await message.reply("✅ User has been <b>banned</b> from the group.")

    for word in unban_words:
        if word in command:
            await _.unban_chat_member(chat_id, user_id)
            return await message.reply("✅ User has been <b>unbanned</b>.")

    for word in kick_words:
        if word in command:
            if user_id in SUDOERS:
                return await message.reply(random.choice(sudo_protect_texts))
            await _.ban_chat_member(chat_id, user_id)
            await _.unban_chat_member(chat_id, user_id)
            return await message.reply("👢 User has been <b>kicked</b> out.")

    for word in mute_words:
        if word in command:
            if user_id in SUDOERS:
                return await message.reply(random.choice(sudo_protect_texts))
            permissions = ChatPermissions(can_send_messages=False)
            await message.chat.restrict_member(user_id, permissions)
            return await message.reply("🔇 User has been <b>muted</b>.")

    for word in unmute_words:
        if word in command:
            permissions = ChatPermissions(can_send_messages=True)
            await message.chat.restrict_member(user_id, permissions)
            return await message.reply("🔊 User has been <b>unmuted</b>.")

    for word in promote_words:
        if word in command:
            await _.promote_chat_member(chat_id, user_id, privileges=ChatPrivileges(
                can_change_info=False,
                can_invite_users=True,
                can_delete_messages=True,
                can_restrict_members=False,
                can_pin_messages=True,
                can_promote_members=False,
                can_manage_chat=True,
                can_manage_video_chats=True,
            ))
            return await message.reply("🔧 User <b>promoted</b> with limited admin rights.")

    for word in fullpromote_words:
        if word in command:
            await _.promote_chat_member(chat_id, user_id, privileges=ChatPrivileges(
                can_change_info=True,
                can_invite_users=True,
                can_delete_messages=True,
                can_restrict_members=True,
                can_pin_messages=True,
                can_promote_members=True,
                can_manage_chat=True,
                can_manage_video_chats=True,
            ))
            return await message.reply("👑 User <b>fully promoted</b> with all admin rights.")

    for word in demote_words:
        if word in command:
            await _.promote_chat_member(chat_id, user_id, privileges=ChatPrivileges(
                can_change_info=False,
                can_invite_users=False,
                can_delete_messages=False,
                can_restrict_members=False,
                can_pin_messages=False,
                can_promote_members=False,
                can_manage_chat=False,
                can_manage_video_chats=False,
            ))
            return await message.reply("📉 User <b>demoted</b> from admin.")

    # If none of the keywords matched
    return await message.reply_text(usage_text)
