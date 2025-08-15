# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import os
import requests
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from Audify import app


def upload_file(file_path: str):
    url = "https://catbox.moe/user/api.php"
    data = {"reqtype": "fileupload"}
    files = {"fileToUpload": open(file_path, "rb")}
    try:
        response = requests.post(url, data=data, files=files)
        if response.status_code == 200:
            link = response.text.strip()
            if link.startswith("https://") or link.startswith("http://"):
                return True, link
            else:
                return False, f"❌ Unexpected response:\n\n<code>{response.text}</code>"
        return False, f"❌ Upload failed\n\n<b>Status:</b> {response.status_code}\n<b>Message:</b> {response.text}"
    except Exception as e:
        return False, f"❌ Exception while uploading\n\n<b>Reason:</b> {str(e)}"


@app.on_message(filters.command(["tgm", "tgt", "telegraph", "tl"]))
async def telegraph_upload_handler(client, message):
    if not message.reply_to_message:
        return await message.reply_text(
            "📎 <b>Please reply to a media file to upload it on Telegraph.</b>"
        )

    media = message.reply_to_message
    file_size = getattr(media.photo, "file_size", 0) or getattr(media.video, "file_size", 0) or getattr(media.document, "file_size", 0)

    if file_size > 200 * 1024 * 1024:
        return await message.reply_text("⚠️ File size exceeds the 200 MB limit.")

    status = await message.reply_text("⏳ <i>Processing your file...</i>")

    try:
        async def progress(current, total):
            try:
                await status.edit_text(f"📥 <b>Downloading:</b> {current * 100 / total:.1f}%")
            except:
                pass

        local_path = await media.download(progress=progress)
        await status.edit_text("📤 <b>Uploading to Telegraph...</b>")

        success, result = upload_file(local_path)
        os.remove(local_path)

        if success:
            await status.edit_text(
                f"✅ <b>Upload Successful!</b>\n\n🔗 <a href='{result}'>Click here to view</a>",
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton("🔗 Open Telegraph", url=result)],
                        [InlineKeyboardButton("❌ Close", callback_data="close")]
                    ]
                ),
            )
        else:
            await status.edit_text(result)

    except Exception as e:
        await status.edit_text(f"❌ <b>Upload failed.</b>\n\n<b>Reason:</b> <code>{e}</code>")


@app.on_callback_query(filters.regex("close_upload"))
async def close_upload_callback(_, query: CallbackQuery):
    try:
        await query.message.delete()
    except:
        pass
