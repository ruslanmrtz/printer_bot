from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.keyboards import get_city_ikb, get_now_workshop_ikb, get_web_app

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
    cities = ['Сургут', 'Нефтеюганск']

    await message.answer('Добро пожаловать!✨')

    await message.answer('Для печати этикетки выберите город из списка ниже 👇',
                         reply_markup=await get_city_ikb(cities))
    await state.set_state(FSMService.workplace)


@router.callback_query(F.data == 'city')
async def get_city_select(callback: CallbackQuery, state: FSMContext):
    cities = ['Сургут', 'Нефтеюганск']

    await callback.message.edit_text('Выберите город из списка ниже 👇',
                                            reply_markup=await get_city_ikb(cities))
    await state.set_state(FSMService.workplace)


@router.callback_query(StateFilter(FSMService.workplace))
async def get_login_aurhorize(callback: CallbackQuery, state: FSMContext, bot: Bot):
    l = ["Пролетарский просп., 10/3", "ул. Есенина, 4", "Набережный просп., 10/1"]

    selected_city = callback.data
    await state.update_data(city=selected_city)

    await callback.message.edit_text('Выберите цех 👇',
                                     reply_markup=await get_now_workshop_ikb(l))
    await state.set_state(FSMService.app)


@router.callback_query(F.data == 'workshop')
async def get_workshop_select(callback: CallbackQuery, state: FSMContext):
    l = ["Пролетарский просп., 10/3", "ул. Есенина, 4", "Набережный просп., 10/1"]

    await callback.message.edit_text('Выберите цех 👇',
                                     reply_markup=await get_now_workshop_ikb(l))
    await state.set_state(FSMService.app)


@router.callback_query(StateFilter(FSMService.app))
async def get_app(callback: Message, state: FSMContext):
    selected_workspace = callback.data
    await state.update_data(workspace=selected_workspace)
    user_data = await state.get_data()
    selected_city = user_data.get('city')
    selected_workspace = user_data.get('workspace')

    await callback.message.edit_text(f'Город: <b>{selected_city}</b>\n'
                                     f'Цех: <b>{selected_workspace}</b>\n'
                                     f'Выберите продукты в приложении 👇',
                                     reply_markup=await get_web_app(selected_city, selected_workspace,
                                                                     callback.from_user.id))






