# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------
import httpx
from pyrogram import filters
from pyrogram.types import Message
from Audify import app
API_BASE = "https://api.exchangerate.host"
# /currency command handler
@app.on_message(filters.command("currency") & (filters.group | filters.private))
async def currency_converter(_, message: Message):
    args = message.text.split()
    if len(args) == 2 and args[1].lower() == "list":
        async with httpx.AsyncClient() as client:
            try:
                res = await client.get(f"{API_BASE}/symbols")
                data = res.json()
                symbols = data["symbols"]
                text = "**🌍 Supported Currencies:**\n\n"
                for code, detail in sorted(symbols.items()):
                    text += f"• `{code}` – {detail['description']}\n"
                await message.reply_text(text[:4000])
            except Exception:
                await message.reply_text("❌ Failed to fetch currency list.")
        return
    if len(args) != 4:
        return await message.reply_text(
            "💱 Usage:\n"
            "`/currency [amount] [from] [to]`\n\n"
            "**Example:** `/currency 100 USD INR`"
        )
    try:
        amount = float(args[1])
        base = args[2].upper()
        target = args[3].upper()
    except ValueError:
        return await message.reply_text("❌ Invalid format. Amount must be a number.")
    url = f"{API_BASE}/convert?from={base}&to={target}&amount={amount}"
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            data = response.json()
            if data.get("success") and "result" in data:
                converted = data["result"]
                rate = data["info"]["rate"]
                await message.reply_text(
                    f"💱 **Currency Converter**\n\n"
                    f"🔢 Amount: `{amount}` {base}\n"
                    f"💸 Rate: `1 {base} = {rate:.4f} {target}`\n"
                    f"✅ Converted: `{converted:.2f} {target}`"
                )
            else:
                await message.reply_text("❌ Conversion failed. Please check currency codes.")
        except Exception:
            await message.reply_text("❌ Failed to fetch exchange rate data.")
