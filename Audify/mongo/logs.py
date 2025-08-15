# ---------------------------------------------------------
# Audify Bot - All rights reserved
# ---------------------------------------------------------
# This code is part of the Audify Bot project.
# Unauthorized copying, distribution, or use is prohibited.
# © Graybots™. All rights reserved.
# ---------------------------------------------------------

from Audify.core.mongo import mongodb

log_collection = mongodb.log_channel  # Make sure your MongoDB has this collection

class LogDB:
    async def set_log(self, chat_id: int, log_channel_id: int):
        await log_collection.update_one(
            {"chat_id": chat_id},
            {"$set": {"log_channel_id": log_channel_id}},
            upsert=True
        )

    async def get_log(self, chat_id: int):
        data = await log_collection.find_one({"chat_id": chat_id})
        return data.get("log_channel_id") if data else None

    async def remove_log(self, chat_id: int):
        await log_collection.delete_one({"chat_id": chat_id})


LOG_DB = LogDB()
