from aiogram.utils import executor
from utils.db.db import main_db


async def on_startup(disp):
    await main_db()


if __name__ == "__main__":
    from handlers import dp
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)