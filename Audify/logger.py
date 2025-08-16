import logging
import sys
import io

# Prepare a UTF-8 safe stream for console output. On some Windows terminals
# the default stream encoding (cp1252) cannot encode emoji/unicode characters
# which causes logging to raise UnicodeEncodeError. Wrap the underlying
# buffer with a TextIOWrapper forcing utf-8 and replacement on errors.
stream_handler = None
try:
    # sys.stderr.buffer exists in normal CPython; wrap it to force utf-8
    utf8_err_stream = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")
    stream_handler = logging.StreamHandler(utf8_err_stream)
except Exception:
    # Fall back to default stream handler (best-effort)
    stream_handler = logging.StreamHandler(sys.stderr)

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    handlers=[
        logging.FileHandler("logger.txt", encoding="utf-8"),
        stream_handler,
    ],
)

logging.getLogger("httpx").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pytgcalls").setLevel(logging.ERROR)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
