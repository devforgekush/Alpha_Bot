from typing import Union
from pyrogram import filters, types
from pyrogram.types import InlineKeyboardMarkup, Message, InlineKeyboardButton
from Audify import app
from Audify.utils import help_pannel
from Audify.utils.database import get_lang
from Audify.utils.decorators.language import LanguageStart, languageCB
from Audify.utils.inline.help import help_back_markup, private_help_panel
from config import BANNED_USERS, SUPPORT_CHAT
from strings import get_string, helpers
from Audify.help.buttons import BUTTONS
from Audify.help.helper import Helper

#------------------------------------------------------------------------------------------------------------------------
# MUSIC | MUSIC | MUSIC | MUSIC | MUSIC | MUSIC | MUSIC | MUSIC | MUSIC | MUSIC | MUSIC | MUSIC | MUSIC | MUSIC | MUSIC | 
#------------------------------------------------------------------------------------------------------------------------

@app.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
async def helper_private(
    client: app, update: Union[types.Message, types.CallbackQuery]
):
    is_callback = isinstance(update, types.CallbackQuery)
    if is_callback:
        try:
            await update.answer()
        except:
            pass
        chat_id = update.message.chat.id
        language = await get_lang(chat_id)
        _ = get_string(language)
        keyboard = help_pannel(_, True)
        await update.edit_message_text(
            _["help_1"].format(SUPPORT_CHAT), reply_markup=keyboard
        )
    else:
        try:
            await update.delete()
        except:
            pass
        language = await get_lang(update.chat.id)
        _ = get_string(language)
        keyboard = help_pannel(_)
        await update.reply_text(  # Changed from reply_photo to reply_text
            text=_["help_1"].format(SUPPORT_CHAT),  # Updated with text instead of caption
            reply_markup=keyboard,
        )


@app.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(_["help_2"], reply_markup=InlineKeyboardMarkup(keyboard))

@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@app.on_callback_query(filters.regex("help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]

    # Page Navigation Handling
    if cb == "page2":
        from Audify.utils import help_pannel_page2
        await CallbackQuery.edit_message_text(
            _["help_1"].format(SUPPORT_CHAT),
            reply_markup=help_pannel_page2(_)
        )
        return

    elif cb == "page3":
        from Audify.utils import help_pannel_page3
        await CallbackQuery.edit_message_text(
            _["help_1"].format(SUPPORT_CHAT),
            reply_markup=help_pannel_page3(_)
        )
        return

    elif cb == "page1":
        from Audify.utils import help_pannel
        await CallbackQuery.edit_message_text(
            _["help_1"].format(SUPPORT_CHAT),
            reply_markup=help_pannel(_)
        )
        return

    keyboard = help_back_markup(_, cb)

    # Help Buttons: hb1 - hb15 (You already had)
    if cb == "hb1":
        await CallbackQuery.edit_message_text(helpers.HELP_1, reply_markup=keyboard)
    elif cb == "hb2":
        await CallbackQuery.edit_message_text(helpers.HELP_2, reply_markup=keyboard)
    elif cb == "hb3":
        await CallbackQuery.edit_message_text(helpers.HELP_3, reply_markup=keyboard)
    elif cb == "hb4":
        await CallbackQuery.edit_message_text(helpers.HELP_4, reply_markup=keyboard)
    elif cb == "hb5":
        await CallbackQuery.edit_message_text(helpers.HELP_5, reply_markup=keyboard)
    elif cb == "hb6":
        await CallbackQuery.edit_message_text(helpers.HELP_6, reply_markup=keyboard)
    elif cb == "hb7":
        await CallbackQuery.edit_message_text(helpers.HELP_7, reply_markup=keyboard)
    elif cb == "hb8":
        await CallbackQuery.edit_message_text(helpers.HELP_8, reply_markup=keyboard)
    elif cb == "hb9":
        await CallbackQuery.edit_message_text(helpers.HELP_9, reply_markup=keyboard)
    elif cb == "hb10":
        await CallbackQuery.edit_message_text(helpers.HELP_10, reply_markup=keyboard)
    elif cb == "hb11":
        await CallbackQuery.edit_message_text(helpers.HELP_11, reply_markup=keyboard)
    elif cb == "hb12":
        await CallbackQuery.edit_message_text(helpers.HELP_12, reply_markup=keyboard)
    elif cb == "hb13":
        await CallbackQuery.edit_message_text(helpers.HELP_13, reply_markup=keyboard)
    elif cb == "hb14":
        await CallbackQuery.edit_message_text(helpers.HELP_14, reply_markup=keyboard)
    elif cb == "hb15":
        await CallbackQuery.edit_message_text(helpers.HELP_15, reply_markup=keyboard)
    elif cb == "hb16":
        await CallbackQuery.edit_message_text(helpers.HELP_16, reply_markup=keyboard)
    elif cb == "hb17":
        await CallbackQuery.edit_message_text(helpers.HELP_17, reply_markup=keyboard)
    elif cb == "hb18":
        await CallbackQuery.edit_message_text(helpers.HELP_18, reply_markup=keyboard)
    elif cb == "hb19":
        await CallbackQuery.edit_message_text(helpers.HELP_19, reply_markup=keyboard)
    elif cb == "hb20":
        await CallbackQuery.edit_message_text(helpers.HELP_20, reply_markup=keyboard)
    elif cb == "hb21":
        await CallbackQuery.edit_message_text(helpers.HELP_21, reply_markup=keyboard)
    elif cb == "hb22":
        await CallbackQuery.edit_message_text(helpers.HELP_22, reply_markup=keyboard)
    elif cb == "hb23":
        await CallbackQuery.edit_message_text(helpers.HELP_23, reply_markup=keyboard)
    elif cb == "hb24":
        await CallbackQuery.edit_message_text(helpers.HELP_24, reply_markup=keyboard)
    elif cb == "hb25":
        await CallbackQuery.edit_message_text(helpers.HELP_25, reply_markup=keyboard)
    elif cb == "hb26":
        await CallbackQuery.edit_message_text(helpers.HELP_26, reply_markup=keyboard)
    elif cb == "hb27":
        await CallbackQuery.edit_message_text(helpers.HELP_27, reply_markup=keyboard)
    elif cb == "hb28":
        await CallbackQuery.edit_message_text(helpers.HELP_28, reply_markup=keyboard)
    elif cb == "hb29":
        await CallbackQuery.edit_message_text(helpers.HELP_29, reply_markup=keyboard)
    elif cb == "hb30":
        await CallbackQuery.edit_message_text(helpers.HELP_30, reply_markup=keyboard)
    elif cb == "hb31":
        await CallbackQuery.edit_message_text(helpers.HELP_31, reply_markup=keyboard)
    elif cb == "hb32":
        await CallbackQuery.edit_message_text(helpers.HELP_32, reply_markup=keyboard)
    elif cb == "hb33":
        await CallbackQuery.edit_message_text(helpers.HELP_33, reply_markup=keyboard)
    elif cb == "hb34":
        await CallbackQuery.edit_message_text(helpers.HELP_34, reply_markup=keyboard)
    elif cb == "hb35":
        await CallbackQuery.edit_message_text(helpers.HELP_35, reply_markup=keyboard)
    elif cb == "hb36":
        await CallbackQuery.edit_message_text(helpers.HELP_36, reply_markup=keyboard)
    elif cb == "hb37":
        await CallbackQuery.edit_message_text(helpers.HELP_37, reply_markup=keyboard)
    elif cb == "hb38":
        await CallbackQuery.edit_message_text(helpers.HELP_38, reply_markup=keyboard)
    elif cb == "hb39":
        await CallbackQuery.edit_message_text(helpers.HELP_39, reply_markup=keyboard)
    elif cb == "hb40":
        await CallbackQuery.edit_message_text(helpers.HELP_40, reply_markup=keyboard)
    elif cb == "hb41":
        await CallbackQuery.edit_message_text(helpers.HELP_41, reply_markup=keyboard)
    elif cb == "hb42":
        await CallbackQuery.edit_message_text(helpers.HELP_42, reply_markup=keyboard)
    elif cb == "hb43":
        await CallbackQuery.edit_message_text(helpers.HELP_43, reply_markup=keyboard)
    elif cb == "hb44":
        await CallbackQuery.edit_message_text(helpers.HELP_44, reply_markup=keyboard)
    elif cb == "hb45":
        await CallbackQuery.edit_message_text(helpers.HELP_45, reply_markup=keyboard)
    elif cb == "hb46":
        await CallbackQuery.edit_message_text(helpers.HELP_46, reply_markup=keyboard)
    elif cb == "hb47":
        await CallbackQuery.edit_message_text(helpers.HELP_47, reply_markup=keyboard)
    elif cb == "hb48":
        await CallbackQuery.edit_message_text(helpers.HELP_48, reply_markup=keyboard)
        
    # Future Extension: You can add hb16 to hb51 here just like above if you need.

#------------------------------------------------------------------------------------------------------------------------
# MANAGEMENT | MANAGEMENT | MANAGEMENT | MANAGEMENT | MANAGEMENT | MANAGEMENT | MANAGEMENT | MANAGEMENT | MANAGEMENT | 
#------------------------------------------------------------------------------------------------------------------------

@app.on_callback_query(filters.regex("MANAGEMENT_CP") & ~BANNED_USERS)
async def helper_cb(client, CallbackQuery):
    await CallbackQuery.edit_message_text(Helper.HELP_M, reply_markup=InlineKeyboardMarkup(BUTTONS.MBUTTON))
    
@app.on_callback_query(filters.regex('MANAGEMENT_BACK'))      
async def mb_plugin_button(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    keyboard = InlineKeyboardMarkup(
    [
    [
    InlineKeyboardButton("ʙᴀᴄᴋ", callback_data=f"MANAGEMENT_CP")
    ]
    ]
    )
    if cb == "MANAGEMENT":
        await CallbackQuery.edit_message_text(f"`something errors`",reply_markup=keyboard,parse_mode=enums.ParseMode.MARKDOWN)
    else:
        await CallbackQuery.edit_message_text(getattr(Helper, cb), reply_markup=keyboard)

#------------------------------------------------------------------------------------------------------------------------
# TOOL | TOOL | TOOL | TOOL | TOOL | TOOL | TOOL | TOOL | TOOL | TOOL | TOOL | TOOL | TOOL | TOOL | TOOL | TOOL | TOOL |
#------------------------------------------------------------------------------------------------------------------------

@app.on_callback_query(filters.regex("TOOL_CP") & ~BANNED_USERS)
async def helper_cb(client, CallbackQuery):
    await CallbackQuery.edit_message_text(Helper.HELP_B, reply_markup=InlineKeyboardMarkup(BUTTONS.BBUTTON))


@app.on_callback_query(filters.regex('TOOL_BACK'))      
async def mb_plugin_button(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    keyboard = InlineKeyboardMarkup(
    [
    [
    InlineKeyboardButton("ʙᴀᴄᴋ", callback_data=f"TOOL_CP")
    ]
    ]
    )
    if cb == "TOOL":
        await CallbackQuery.edit_message_text(f"`something errors`",reply_markup=keyboard,parse_mode=enums.ParseMode.MARKDOWN)
    else:
        await CallbackQuery.edit_message_text(getattr(Helper, cb), reply_markup=keyboard)

#------------------------------------------------------------------------------------------------------------------------
# MAIN HELP | MAIN HELP | MAIN HELP | MAIN HELP | MAIN HELP | MAIN HELP | MAIN HELP | MAIN HELP | MAIN HELP | MAIN HELP |
#------------------------------------------------------------------------------------------------------------------------

@app.on_callback_query(filters.regex("MAIN_CP") & ~BANNED_USERS)
async def helper_cb(client, CallbackQuery):
    await CallbackQuery.edit_message_text(Helper.HELP_Audify, reply_markup=InlineKeyboardMarkup(BUTTONS.SBUTTON))

@app.on_callback_query(filters.regex('MAIN_BACK'))      
async def mb_plugin_button(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    keyboard = InlineKeyboardMarkup(
    [
    [
    InlineKeyboardButton("ʙᴀᴄᴋ", callback_data=f"MAIN_CP")
    ]
    ]
    )
    if cb == "MAIN":
        await CallbackQuery.edit_message_text(f"`something errors`",reply_markup=keyboard,parse_mode=enums.ParseMode.MARKDOWN)
    else:
        await CallbackQuery.edit_message_text(getattr(Helper, cb), reply_markup=keyboard)

#------------------------------------------------------------------------------------------------------------------------
# PROMOTION | PROMOTION | PROMOTION | PROMOTION | PROMOTION | PROMOTION | PROMOTION | PROMOTION | PROMOTION | PROMOTION |
#------------------------------------------------------------------------------------------------------------------------

@app.on_callback_query(filters.regex("PROMOTION_CP") & ~BANNED_USERS)
async def helper_cb(client, CallbackQuery):
    await CallbackQuery.edit_message_text(Helper.HELP_PROMOTION, reply_markup=InlineKeyboardMarkup(BUTTONS.PBUTTON))

@app.on_callback_query(filters.regex('PROMOTION_BACK'))      
async def mb_plugin_button(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    keyboard = InlineKeyboardMarkup(
    [
    [
    InlineKeyboardButton("ʙᴀᴄᴋ", callback_data=f"PROMOTION_CP")
    ]
    ]
    )
    if cb == "PROMOTION":
        await CallbackQuery.edit_message_text(f"`something errors`",reply_markup=keyboard,parse_mode=enums.ParseMode.MARKDOWN)
    else:
        await CallbackQuery.edit_message_text(getattr(Helper, cb), reply_markup=keyboard)

#------------------------------------------------------------------------------------------------------------------------
# ALL BOT'S | ALL BOT'S | ALL BOT'S | ALL BOT'S | ALL BOT'S | ALL BOT'S | ALL BOT'S | ALL BOT'S | ALL BOT'S | ALL BOT'S | 
#------------------------------------------------------------------------------------------------------------------------

@app.on_callback_query(filters.regex("ALLBOT_CP") & ~BANNED_USERS)
async def helper_cb(client, CallbackQuery):
    await CallbackQuery.edit_message_text(Helper.HELP_ALLBOT, reply_markup=InlineKeyboardMarkup(BUTTONS.ABUTTON))

@app.on_callback_query(filters.regex('ALLBOT_BACK'))      
async def mb_plugin_button(client, CallbackQuery):
    callback_data = CallbackQuery.data.strip()
    cb = callback_data.split(None, 1)[1]
    keyboard = InlineKeyboardMarkup(
    [
    [
    InlineKeyboardButton("ʙᴀᴄᴋ", callback_data=f"ALLBOT_CP")
    ]
    ]
    )
    if cb == "ALLBOT":
        await CallbackQuery.edit_message_text(f"`something errors`",reply_markup=keyboard,parse_mode=enums.ParseMode.MARKDOWN)
    else:
        await CallbackQuery.edit_message_text(getattr(Helper, cb), reply_markup=keyboard)

#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------
