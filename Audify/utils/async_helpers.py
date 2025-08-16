import asyncio
import threading
from typing import Coroutine, Any


def start_background_task(coro: Coroutine[Any, Any, Any]) -> None:
    """Start a coroutine in a running event loop if available, otherwise
    create a background loop in a daemon thread and schedule the coroutine.

    This is intended for long-running background jobs that were previously
    started at module-import time with `asyncio.create_task(...)`.
    """
    try:
        loop = asyncio.get_running_loop()
        loop.create_task(coro)
        return
    except RuntimeError:
        # No running loop in this thread; fall back to a dedicated background loop
        bg_loop = asyncio.new_event_loop()

        def _run_loop():
            try:
                asyncio.set_event_loop(bg_loop)
                # schedule the coroutine and run loop forever
                bg_loop.create_task(coro)
                bg_loop.run_forever()
            finally:
                try:
                    bg_loop.close()
                except Exception:
                    pass

        t = threading.Thread(target=_run_loop, daemon=True)
        t.start()
