from Audify.core.bot import Alphabot
from Audify.core.dir import dirr
from Audify.core.git import git
from Audify.core.userbot import Userbot
from Audify.misc import dbb, heroku
from Audify.mongo.logs import LOG_DB

from SafoneAPI import SafoneAPI
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
