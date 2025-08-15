# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

import math
from pyrogram import filters
from pyrogram.types import Message
from Audify import app

# Safe dictionary of allowed functions
SAFE_FUNCTIONS = {
    "abs": abs,
    "round": round,
    "ceil": math.ceil,
    "floor": math.floor,
    "sqrt": math.sqrt,
    "sin": lambda x: math.sin(math.radians(x)),
    "cos": lambda x: math.cos(math.radians(x)),
    "tan": lambda x: math.tan(math.radians(x)),
    "log": math.log,
    "log10": math.log10,
    "exp": math.exp,
    "pi": math.pi,
    "e": math.e,
    "__builtins__": None,
}

# 🔢 /calculate or /calc command handler
@app.on_message(filters.command(["calculate", "calc"]) & filters.private)
async def calculate_handler(_, message: Message):
    if len(message.command) < 2:
        return await message.reply("🔢 Usage: `/calc <expression>`\n\nExample: `/calc (5 + 3) * 2`", quote=True)
    
    expression = message.text.split(None, 1)[1]

    try:
        result = eval(expression, SAFE_FUNCTIONS)
        await message.reply(f"🧮 **Expression:** `{expression}`\n✅ **Result:** `{result}`", quote=True)
    except Exception as e:
        await message.reply(f"❌ Invalid expression.\n\n`{str(e)}`", quote=True)
