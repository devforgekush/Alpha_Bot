# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from pyrogram import Client, filters, enums
from pyrogram.types import Message
import traceback
from Audify import app


@app.on_message(filters.command("python"))
async def execute_python_code(client, message: Message):
    if len(message.command) < 2:
        await message.reply(
            "❗ Please enter your Python code after the command.\n\n"
            "💡 Example: <code>/python print('Hello, World!')</code>",
            parse_mode=enums.ParseMode.HTML
        )
        return

    python_code = " ".join(message.command[1:])

    try:
        # ⚠️ WARNING: Using `exec()` is dangerous. Do not expose this to untrusted users.
        local_vars = {}
        exec(python_code, {}, local_vars)
        result = local_vars.get('result', '✅ Code executed successfully.')
        await message.reply(
            f"<b>Execution Result:</b>\n<code>{result}</code>",
            parse_mode=enums.ParseMode.HTML
        )
    except Exception as e:
        traceback_str = traceback.format_exc()
        await message.reply(
            f"<b>⚠️ Code Execution Error:</b>\n<code>{str(e)}</code>\n\n<b>Traceback:</b>\n<code>{traceback_str}</code>",
            parse_mode=enums.ParseMode.HTML
        )
