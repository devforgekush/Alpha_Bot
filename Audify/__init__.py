from Audify.core.bot import Alphabot
from Audify.core.dir import dirr
from Audify.core.git import git
from Audify.core.userbot import Userbot
from Audify.misc import dbb, heroku
from Audify.mongo.logs import LOG_DB

# Make SafoneAPI optional
try:
    from SafoneAPI import SafoneAPI
    SAFONE_AVAILABLE = True
except ImportError:
    print("⚠️ SafoneAPI not available - some features may be limited")
    SAFONE_AVAILABLE = False
    # Create a dummy class
    class SafoneAPI:
        def __init__(self):
            pass

from .logger import LOGGER

dirr()
git()
dbb()
heroku()

app = Alphabot()
api = SafoneAPI()
userbot = Userbot()


from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
