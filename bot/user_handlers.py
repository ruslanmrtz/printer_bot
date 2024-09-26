from aiogram import Router, Bot, F, types
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

    person = State()
    city = State()      # Выбор города
    workplace = State()  # Выбор цеха
    app = State()


@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext) -> None:

    await message.answer('Добро пожаловать!✨')

    button = types.KeyboardButton(text="Отправить номер телефона 📱", request_contact=True)
    keyboard = types.ReplyKeyboardMarkup(keyboard=[[button]], resize_keyboard=True, one_time_keyboard=True)

    reg_msg = await message.answer('Для регистрации предлагаю вам отправить свой номер, нажав на кнопку.',
                         reply_markup=keyboard)
    reg_id = reg_msg.message_id

    await state.update_data(reg_id=reg_id)

    await state.set_state(FSMService.person)


@router.message(StateFilter(FSMService.person))
async def contacts(msg: types.Message, bot: Bot, state: FSMContext):
    if msg.contact:
        user_id = msg.from_user.id
        phone_number = msg.contact.phone_number
        data = await state.get_data()
        reg_id = data.get('reg_id')

        # Сохраняем данные в базу
        await bot_db.add_user(str(phone_number), str(user_id))

        await bot.delete_message(chat_id=user_id, message_id=msg.message_id)
        await bot.delete_message(chat_id=user_id, message_id=reg_id)

        await msg.answer('Для печати этикетки выберите город из списка ниже 👇',
                                         reply_markup=await get_city_ikb())

        await state.set_state(FSMService.app)

    else:
        await msg.answer("Пожалуйста, отправьте ваш номер телефона, используя кнопку.")


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
    print('Проверка продуктов на истечение срока годности')

    # Открываем сессию для работы с базой данных
    async with bot_db.AsyncSessionLocal() as session:
        # Выполняем SQL-запрос для получения списка продуктов
        result = await session.execute(text("SELECT id, city, workshop, product_name, user_id, time_end FROM products"))
        products = result.fetchall()

        # Получаем текущее время
        now = datetime.now()

        # Проходим по списку продуктов
        for product_id, city, workshop, product_name, user_id, time_end in products:
            # Если продукт истекает в течение часа
            if now <= time_end <= now + timedelta(hours=1):
                # Отправляем пользователю уведомление о скором истечении срока годности

                if workshop:
                    await bot.send_message(
                        user_id,
                        f"⚠️ <b>Город</b>: {city} \n"
                        f"⚠️ <b>Цех</b>: {workshop}\n"
                        f"⚠️ <b>Продукт</b>: '{product_name}'\n испортится в {time_end.strftime('%H:%M %d-%m-%Y')}"
                    )
                else:
                    await bot.send_message(
                        user_id,
                        f"⚠️ <b>Город</b>: {city} \n"
                        f"⚠️ <b>Продукт</b>: '{product_name}'\n испортится в {time_end.strftime('%H:%M %d-%m-%Y')}"
                    )

                # Удаляем запись о продукте по id из базы данных
                await session.execute(text("DELETE FROM products WHERE id = :id"), {'id': product_id})

        # Сохраняем изменения в базе данных
        await session.commit()

