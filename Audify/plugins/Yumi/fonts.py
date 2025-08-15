# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Audify.utils.Audify_font import Fonts
from Audify import app

# Font map with proper names for visual button labels
font_map = {
    "typewriter": ("𝚃𝚢𝚙𝚎𝚠𝚛𝚒𝚝𝚎𝚛", Fonts.typewriter),
    "outline": ("𝕆𝕦𝕥𝕝𝕚𝕟𝕖", Fonts.outline),
    "serif": ("𝐒𝐞𝐫𝐢𝐟", Fonts.serief),
    "bold_cool": ("𝑺𝒆𝒓𝒊𝒇", Fonts.bold_cool),
    "cool": ("𝑆𝑒𝑟𝑖𝑓", Fonts.cool),
    "small_cap": ("Sᴍᴀʟʟ Cᴀᴘs", Fonts.smallcap),
    "script": ("𝓈𝒸𝓇𝒾𝓅𝓉", Fonts.script),
    "script_bolt": ("𝓼𝓬𝓻𝓲𝓹𝓽", Fonts.bold_script),
    "tiny": ("ᵗⁱⁿʸ", Fonts.tiny),
    "comic": ("ᑕOᗰIᑕ", Fonts.comic),
    "sans": ("𝗦𝗮𝗻𝘀", Fonts.san),
    "slant_sans": ("𝙎𝙖𝙣𝙨", Fonts.slant_san),
    "slant": ("𝘚𝘢𝘯𝘴", Fonts.slant),
    "sim": ("𝖲𝖺𝗇𝗌", Fonts.sim),
    "circles": ("Ⓒ︎Ⓘ︎Ⓡ︎Ⓒ︎Ⓛ︎Ⓔ︎Ⓢ︎", Fonts.circles),
    "circle_dark": ("🅒︎🅘︎🅡︎🅒︎🅛︎🅔︎🅢︎", Fonts.dark_circle),
    "gothic": ("𝔊𝔬𝔱𝔥𝔦𝔠", Fonts.gothic),
    "gothic_bolt": ("𝕲𝖔𝖙𝖍𝖎𝖈", Fonts.bold_gothic),
    "cloud": ("C͜͡l͜͡o͜͡u͜͡d͜͡s͜͡", Fonts.cloud),
    "happy": ("H̆̈ă̈p̆̈p̆̈y̆̈", Fonts.happy),
    "sad": ("S̑̈ȃ̈d̑̈", Fonts.sad),
    "special": ("Special", Fonts.special),
    "squares": ("🅂🅀🅄🄰🅁🄴🅂", Fonts.square),
    "squares_bold": ("🆂︎🆀︎🆄︎🅰︎🆁︎🅴︎🆂︎", Fonts.dark_square),
    "andalucia": ("ꪖꪀᦔꪖꪶꪊᥴ𝓲ꪖ", Fonts.andalucia),
    "manga": ("爪卂几ᘜ卂", Fonts.manga),
    "stinky": ("S̾t̾i̾n̾k̾y̾", Fonts.stinky),
    "bubbles": ("B̥ͦu̥ͦb̥ͦb̥ͦl̥ͦe̥ͦs̥ͦ", Fonts.bubbles),
    "underline": ("U͟n͟d͟e͟r͟l͟i͟n͟e͟", Fonts.underline),
    "ladybug": ("꒒ꍏꀷꌩꌃꀎꁅ", Fonts.ladybug),
    "rays": ("R҉a҉y҉s҉", Fonts.rays),
    "birds": ("B҈i҈r҈d҈s҈", Fonts.birds),
    "slash": ("S̸l̸a̸s̸h̸", Fonts.slash),
    "stop": ("s⃠t⃠o⃠p⃠", Fonts.stop),
    "skyline": ("S̺͆k̺͆y̺͆l̺͆i̺͆n̺͆e̺͆", Fonts.skyline),
    "arrows": ("A͎r͎r͎o͎w͎s͎", Fonts.arrows),
    "qvnes": ("ዪሀክቿነ", Fonts.rvnes),
    "strike": ("S̶t̶r̶i̶k̶e̶", Fonts.strike),
    "frozen": ("F༙r༙o༙z༙e༙n༙", Fonts.frozen),
}

def generate_buttons(page=1):
    per_page = 15
    keys = list(font_map.items())
    start = (page - 1) * per_page
    end = start + per_page
    sliced = keys[start:end]

    buttons = []
    for i in range(0, len(sliced), 3):
        row = [
            InlineKeyboardButton(name, callback_data=f"style+{key}")
            for key, (name, _) in sliced[i:i+3]
        ]
        buttons.append(row)

    nav = []
    if start > 0:
        nav.append(InlineKeyboardButton("⏪ Back", callback_data=f"fontpage+{page-1}"))
    if end < len(keys):
        nav.append(InlineKeyboardButton("Next ⏩", callback_data=f"fontpage+{page+1}"))
    nav.append(InlineKeyboardButton("✖️ Close", callback_data="close"))
    buttons.append(nav)
    return buttons

@app.on_message(filters.command(["font", "fonts"]))
async def style_buttons(c, m):
    if len(m.text.split(" ", 1)) < 2:
        return await m.reply_text("Please provide some text after the `/fonts` command.")
    text = m.text.split(" ", 1)[1]
    buttons = generate_buttons(page=1)
    await m.reply_text(f"`{text}`", reply_markup=InlineKeyboardMarkup(buttons), quote=True)

@app.on_callback_query(filters.regex("^fontpage"))
async def paginate(c, m):
    await m.answer()
    page = int(m.data.split("+")[1])
    buttons = generate_buttons(page)
    await m.message.edit_reply_markup(InlineKeyboardMarkup(buttons))

@app.on_callback_query(filters.regex("^style"))
async def style(c, m):
    await m.answer()
    _, style_key = m.data.split("+")
    if style_key not in font_map:
        return
    font_func = font_map[style_key][1]
    try:
        text = m.message.reply_to_message.text
        styled = font_func(text.split(" ", 1)[1])
        await m.message.edit_text(styled, reply_markup=m.message.reply_markup)
    except:
        pass
