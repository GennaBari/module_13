from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import  FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import asyncio

api = ""
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


class UserState(StatesGroup):
     age = State()
     growth = State()
     weight = State()
     gender = State()

@dp.message_handler(commands = 'start')
async def start_message(message):
    button1 = KeyboardButton(text='Рассчитать')
    button2 = KeyboardButton(text='Информация')
    keyboard = ReplyKeyboardMarkup(
        resize_keyboard=True,
        input_field_placeholder='Введите данные здесь')
    keyboard.add(button1)
    keyboard.add(button2)
    await message.answer ('Привет! Я бот, помогающий твоему здоровью')

@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer(
        'Этот бот помогает рассчитать сколько вам необходимо потреблять ежедневно калорий.'
    )

@dp.message_handler(text='Рассчитать')
async def set_gender(message):
    await message.answer('Назовите свой пол: men/women')
    await UserState.gender.set()

@dp.message_handler(state=UserState.gender)
async def set_age(message):
    await message.answer('Введите свой возраст:')
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer(f'Введите свой рост(cм):')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer(f'Введите свой вес(кг):')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()

    try:
        age = float(data['age'])
        growth = float(data['growth'])
        weight = float(data['weight'])
    except:
        await message.answer(f'Не могу конвертировать введенные значения в числа.')
        await state.finish()
        return

    #формула Миффлина-Сен-Жерона для подсчета нормы каллорий
    #для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5
    calories_man = 10 * weight + 6.25 * growth - 5 * age + 5
    # для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161
    calories_wom = 10 * weight + 6.25 * growth - 5 * age - 161
    await message.answer(f'Норма (муж.): {calories_man} ккал')
    await message.answer(f'Норма (жен.): {calories_wom} ккал')
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
