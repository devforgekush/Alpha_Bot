from traceback import format_exc
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

try:
    from search_engine_parser.core.engines.google import Search as GoogleSearch
    from search_engine_parser.core.engines.stackoverflow import Search as StackSearch
    from search_engine_parser.core.exceptions import NoResultsFound, NoResultsOrTrafficError
except Exception:
    GoogleSearch = None
    StackSearch = None
    NoResultsFound = Exception
    NoResultsOrTrafficError = Exception

from Audify import app

# Initialize search engines if available
gsearch = GoogleSearch() if GoogleSearch else None
stsearch = StackSearch() if StackSearch else None


def build_keyboard(results):
    buttons = []
    for result in results[:5]:
        title = result.get("titles", "Result")
        url = result.get("links", "#")
        buttons.append([InlineKeyboardButton(text=title, url=url)])

    buttons.append([
        InlineKeyboardButton("❌ Close", callback_data="close")
    ])
    return InlineKeyboardMarkup(buttons)


@app.on_message(filters.command("google"))
async def search_google(app, msg: Message):
    if not gsearch:
        return await msg.reply_text("⚠️ Feature unavailable: missing dependency 'search_engine_parser'.")
    query = msg.text.split(None, 1)
    if len(query) == 1:
        return await msg.reply_text("🔍 Please provide something to search.")
    
    wait_msg = await msg.reply_text("🔎 Searching Google...")
    try:
        results = await gsearch.async_search(query[1])
        keyboard = build_keyboard(results)
        await wait_msg.delete()
        await msg.reply_text(
            f"🔗 Here are the top results for: **{query[1].title()}**",
            reply_markup=keyboard
        )
    except NoResultsFound:
        await wait_msg.delete()
        await msg.reply_text("❌ No results found for your query.")
    except NoResultsOrTrafficError:
        await wait_msg.delete()
        await msg.reply_text("🚫 Google temporarily blocked traffic. Try again later.")
    except Exception as e:
        await wait_msg.delete()
        await msg.reply_text("⚠️ Something went wrong while searching. Try again later.")
    from Audify.logger import LOGGER
    LOGGER(__name__).error(f"[ERROR - Google Search]: {e}\n{format_exc()}")


@app.on_message(filters.command("stack"))
async def search_stackoverflow(app, msg: Message):
    if not stsearch:
        return await msg.reply_text("⚠️ Feature unavailable: missing dependency 'search_engine_parser'.")
    query = msg.text.split(None, 1)
    if len(query) == 1:
        return await msg.reply_text("📘 Please provide a query to search StackOverflow.")
    
    wait_msg = await msg.reply_text("💻 Searching StackOverflow...")
    try:
        results = await stsearch.async_search(query[1])
        keyboard = build_keyboard(results)
        await wait_msg.delete()
        await msg.reply_text(
            f"🧠 StackOverflow results for: **{query[1].title()}**",
            reply_markup=keyboard
        )
    except NoResultsFound:
        await wait_msg.delete()
        await msg.reply_text("❌ No StackOverflow results found for your query.")
    except NoResultsOrTrafficError:
        await wait_msg.delete()
        await msg.reply_text("🚫 StackOverflow is under traffic pressure. Try again soon.")
    except Exception as e:
        await wait_msg.delete()
        await msg.reply_text("⚠️ Something went wrong. Please report to @iam_Audify.")
    LOGGER(__name__).error(f"[ERROR - Stack Search]: {e}\n{format_exc()}")
