import asyncio
import importlib
import threading
import time
import requests

from pyrogram import idle

# Try to import pytgcalls, make it optional
try:
    from pytgcalls.exceptions import NoActiveGroupCall
    PYTGCALLS_AVAILABLE = True
except ImportError:
    NoActiveGroupCall = Exception  # Fallback exception
    PYTGCALLS_AVAILABLE = False

# Try to import config from different locations
try:
    import config
    print("✅ Imported config from root directory")
except ImportError:
    try:
        from Audify import config
        print("✅ Imported config from Audify package")
    except ImportError:
        print("❌ Failed to import config from both locations")
        raise

from Audify import LOGGER, app, userbot
from Audify.core.call import Audify
from Audify.misc import sudo
from Audify.plugins import ALL_MODULES
from Audify.utils.database import get_banned_users, get_gbanned
from config import BANNED_USERS

# Import web server
try:
    from web_server import start_web_server
    WEB_SERVER_AVAILABLE = True
except ImportError:
    WEB_SERVER_AVAILABLE = False
    LOGGER(__name__).warning("⚠️ Web server module not available")


def start_pinger():
    def ping_loop():
        url = getattr(config, "RAILWAY_URL", None)
        if not url:
            LOGGER(__name__).info("ℹ️ RAILWAY_URL not set, pinger disabled")
            return
        LOGGER(__name__).info(f"🚀 Starting pinger for: {url}")
        # Configurable values (can be set in config.py)
        interval = getattr(config, "PING_INTERVAL", 720)  # seconds between pings
        timeout = getattr(config, "PING_TIMEOUT", 10)
        retries = getattr(config, "PING_RETRIES", 3)
        retry_backoff = getattr(config, "PING_RETRY_BACKOFF", 2)  # seconds

        session = requests.Session()
        consecutive_failures = 0

        while True:
            try:
                last_status = None
                # Try a few times for transient server errors (502/503/504)
                for attempt in range(1, retries + 1):
                    try:
                        response = session.get(url, timeout=timeout)
                        last_status = response.status_code
                        if response.status_code == 200:
                            consecutive_failures = 0
                            LOGGER(__name__).debug("✅ Pinger: App is alive")
                            break
                        # treat some 5xx responses as transient and retry
                        if response.status_code in (502, 503, 504) and attempt < retries:
                            LOGGER(__name__).debug(f"🔁 Pinger: transient {response.status_code}, retry {attempt}/{retries}")
                            time.sleep(retry_backoff)
                            continue
                        # non-OK, non-transient or exhausted retries
                        consecutive_failures += 1
                        # Only log a warning every few failures to avoid noise
                        if consecutive_failures == 1 or consecutive_failures % 3 == 0:
                            LOGGER(__name__).warning(f"⚠️ Pinger: Unexpected status {response.status_code} (failures={consecutive_failures})")
                        break
                    except requests.exceptions.RequestException as e:
                        last_status = type(e).__name__
                        # on request exceptions, retry unless out of attempts
                        if attempt < retries:
                            LOGGER(__name__).debug(f"🔁 Pinger: request exception {type(e).__name__}, retry {attempt}/{retries}")
                            time.sleep(retry_backoff)
                            continue
                        consecutive_failures += 1
                        LOGGER(__name__).warning(f"⚠️ Pinger failed: {type(e).__name__} (failures={consecutive_failures})")
                        break
            except Exception as e:
                # Unexpected error in the ping loop itself
                consecutive_failures += 1
                LOGGER(__name__).error(f"❌ Pinger error: {type(e).__name__} (failures={consecutive_failures})")
            # Sleep before next cycle
            time.sleep(interval)
    t = threading.Thread(target=ping_loop, daemon=True)
    t.start()
    LOGGER(__name__).info("🔄 Pinger thread started")

async def init():
    if (
        not config.STRING1
        and not config.STRING2
        and not config.STRING3
        and not config.STRING4
        and not config.STRING5
    ):
        LOGGER(__name__).error("🚫 String Session Missing! Please configure at least one Pyrogram session string.")
        LOGGER(__name__).warning("⚠️ Bot will continue running but may have limited functionality")
    
    # Start web server for Railway health checks
    if WEB_SERVER_AVAILABLE:
        try:
            port = int(getattr(config, "PORT", 8000))
            start_web_server(port)
            LOGGER(__name__).info(f"🌐 Web server started on port {port}")
        except Exception as e:
            LOGGER(__name__).warning(f"⚠️ Failed to start web server: {e}")
    
    start_pinger()
    await sudo()
    try:
        users = await get_gbanned()
        for user_id in users:
            BANNED_USERS.add(user_id)
        users = await get_banned_users()
        for user_id in users:
            BANNED_USERS.add(user_id)
    except:
        pass
    await app.start()
    import traceback
    for all_module in ALL_MODULES:
        try:
            importlib.import_module("Audify.plugins" + all_module)
            LOGGER("Audify.plugins").debug(f"✅ Loaded module: {all_module}")
        except Exception as e:
            tb = traceback.format_exc()
            LOGGER("Audify.plugins").error(
                f"❌ Failed to load module {all_module}: {type(e).__name__} - {e}\nTraceback:\n{tb}"
            )
    LOGGER("Audify.plugins").info("✅ All modules successfully loaded. Alphabot is ready to serve 🎶")
    await userbot.start()
    
    # Initialize Audify only if pytgcalls is available
    if PYTGCALLS_AVAILABLE:
        await Audify.start()
        try:
            await Audify.stream_call("https://te.legra.ph/file/29f784eb49d230ab62e9e.mp4")
        except NoActiveGroupCall:
            LOGGER("Audify").warning(
                "📢 Please start a voice chat in your log group or linked channel!\n\n⚠️ Alphabot cannot stream without an active group call."
            )
            LOGGER("Audify").info("ℹ️ Bot will continue running without streaming capability")
        except:
            pass
        await Audify.decorators()
        LOGGER("Audify").info(
            "🎧 Alphabot Music Bot started successfully with voice support.\n🛡️ Developed with passion by @devforgekush 💻"
        )
    else:
        LOGGER("Audify").warning("⚠️ pytgcalls not available - voice features disabled")
        LOGGER("Audify").info(
            "🎧 Alphabot Music Bot started successfully (voice features disabled).\n🛡️ Developed with passion by @devforgekush 💻"
        )
    
    await idle()
    await app.stop()
    await userbot.stop()
    if PYTGCALLS_AVAILABLE:
        await Audify.stop()
    LOGGER("Audify").info("🛑 Alphabot Music Bot has stopped. See you soon! 👋")


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init())
