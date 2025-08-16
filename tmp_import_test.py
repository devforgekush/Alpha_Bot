import sys
import asyncio
import importlib
import traceback
import logging

# Ensure UTF-8 stdout to avoid UnicodeEncodeError on Windows console
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
if hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Start an asyncio event loop in a background thread so modules that
# call asyncio.create_task(...) at import time find a running loop.
loop = asyncio.new_event_loop()

def _run_loop():
    try:
        asyncio.set_event_loop(loop)
        loop.run_forever()
    except Exception:
        pass

import threading
loop_thread = threading.Thread(target=_run_loop, daemon=True)
loop_thread.start()

# Reduce logging noise during tests
logging.getLogger().setLevel(logging.CRITICAL)

from Audify.plugins import ALL_MODULES

errs = {}
for m in ALL_MODULES:
    try:
        importlib.import_module('Audify.plugins' + m)
    except Exception:
        errs[m] = traceback.format_exc()

for k, v in errs.items():
    print('---MODULE', k)
    print(v)

# Close loop cleanly
try:
    # stop background loop
    loop.call_soon_threadsafe(loop.stop)
    loop_thread.join(timeout=1)
finally:
    try:
        loop.close()
    except Exception:
        pass
