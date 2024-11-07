from aiogram import Bot, Dispatcher, executor, types
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


api = "7715838785:AAHWFuxFItqRsoetC_dgSd60OW9ke6lK_c8"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


@dp.message_handler(commands=['start'])
async def start_messages(message):
       await message.answer('Привет! Я бот помогающий твоему здоровью.')



@dp.message_handler()
async def all_messages(message):
        await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)