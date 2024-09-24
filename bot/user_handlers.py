from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import datetime, timedelta
from sqlalchemy import text

from bot import bot_db
from bot.keyboards import get_city_ikb, get_now_workshop_ikb, get_web_app

from cities import get_workshop

router = Router()


class FSMService(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем

    city = State()      # Выбор города
    workplace = State()  # Выбор цеха
    app = State()


@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext) -> None:

    await message.answer('Добро пожаловать!✨')

    await state.set_state(FSMService.city)

    await message.answer('Для печати этикетки выберите город из списка ниже 👇',
                         reply_markup=await get_city_ikb())
    await state.set_state(FSMService.app)


@router.callback_query(F.data == 'city')
async def get_city_select(callback: CallbackQuery, state: FSMContext):

    await callback.message.edit_text('Для печати этикетки выберите город из списка ниже 👇',
                         reply_markup=await get_city_ikb())
    await state.set_state(FSMService.app)


@router.callback_query(F.data == 'Сургут')
async def get_login_aurhorize(callback: CallbackQuery, state: FSMContext, bot: Bot):

    selected_city = callback.data
    await state.update_data(city=selected_city)

    await callback.message.edit_text('Выберите цех 👇',
                                     reply_markup=await get_now_workshop_ikb())
    await state.set_state(FSMService.app)


@router.callback_query(StateFilter(FSMService.app))
async def get_app(callback: Message, state: FSMContext):

    # Для Сургута, т.к цеха есть
    if callback.data in await get_workshop():
        user_data = await state.get_data()
        selected_city = user_data.get('city')
        selected_workspace = callback.data

        await callback.message.edit_text(f'Город: <b>{selected_city}</b>\n'
                                         f'Цех: <b>{selected_workspace}</b>\n'
                                         f'Выберите продукты в приложении 👇',
                                         reply_markup=await get_web_app(selected_city, selected_workspace,
                                                                        callback.from_user.id))
    # Для любого другого города
    else:
        selected_city = callback.data
        await state.update_data(city=selected_city)
        await callback.message.edit_text(f'Город: <b>{selected_city}</b>\n'
                                         f'Выберите продукты в приложении 👇',
                                         reply_markup=await get_web_app(selected_city, '',
                                                                        callback.from_user.id))


async def check_expired_products(bot: Bot):
    print('Проверка')
    async with bot_db.AsyncSessionLocal() as session:
        result = await session.execute(text("SELECT product_name, user_id, time_end FROM products"))
        products = result.fetchall()

        now = datetime.now()

        for product_name, user_id, time_end in products:
            if now <= time_end <= now + timedelta(hours=1):
                await bot.send_message(
                    user_id,
                    f"⚠️ Продукт '{product_name}' испортится в {time_end.strftime('%H:%M %d-%m-%Y')}")

