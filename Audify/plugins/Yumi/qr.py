from pyrogram import Client, filters
from pyrogram.types import Message
from Audify import app
from PIL import Image
import io
import io

# qrcode optional
try:
    import qrcode
except ImportError:
    qrcode = None

# Generate a QR code from input text
def generate_qr_code(text):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)

    img = qr.make_image(fill_color="white", back_color="black")

    # Save QR to bytes for sending
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    return img_bytes


@app.on_message(filters.command("qr"))
async def qr_handler(client: Client, message: Message):
    command_text = message.command
    if len(command_text) > 1:
        if not qrcode:
            return await message.reply_text("⚠️ Feature unavailable: missing dependency 'qrcode'.")
        input_text = " ".join(command_text[1:])
        qr_image = generate_qr_code(input_text)
        await message.reply_photo(qr_image, caption="🧾 Here's your QR Code.")
    else:
        await message.reply_text(
            "❗ Please provide text after the command.\n\n"
            "💡 Example: <code>/qr https://example.com</code>",
            parse_mode="html"
        )
