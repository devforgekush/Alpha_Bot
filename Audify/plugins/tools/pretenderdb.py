# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from typing import Optional, Tuple
from motor.motor_asyncio import AsyncIOMotorClient as MongoCli
from config import MONGO_DB_URI

# ─── MongoDB Setup ─── #
mongo = MongoCli(MONGO_DB_URI).Rankings
impdb = mongo.pretender


# ─── User Data Management ─── #
async def usr_data(user_id: int) -> bool:
    """Check if user exists in database."""
    return await impdb.find_one({"user_id": user_id}) is not None


async def get_userdata(user_id: int) -> Optional[Tuple[str, str, str]]:
    """Retrieve username, first name, and last name."""
    user = await impdb.find_one({"user_id": user_id})
    if user:
        return user.get("username"), user.get("first_name"), user.get("last_name")
    return None


async def add_userdata(user_id: int, username: str, first_name: str, last_name: str):
    """Insert or update user data."""
    await impdb.update_one(
        {"user_id": user_id},
        {
            "$set": {
                "username": username,
                "first_name": first_name,
                "last_name": last_name,
            }
        },
        upsert=True,
    )


# ─── Pretender Chat Toggle ─── #
async def check_pretender(chat_id: int) -> bool:
    """Check if pretender toggle is enabled for a chat."""
    return await impdb.find_one({"chat_id_toggle": chat_id}) is not None


async def impo_on(chat_id: int):
    """Enable pretender toggle for a chat."""
    await impdb.insert_one({"chat_id_toggle": chat_id})


async def impo_off(chat_id: int):
    """Disable pretender toggle for a chat."""
    await impdb.delete_one({"chat_id_toggle": chat_id})
