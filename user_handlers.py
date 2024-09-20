from aiogram import Router, F, Bot
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards import get_city_ikb, get_now_workshop_ikb, get_web_app

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

    cities = ['Сургут']

    await message.answer('Добро пожаловать!\nДля печати этикетки выберите город из списка ниже 👇',
                         reply_markup=await get_city_ikb(cities))
    await state.set_state(FSMService.workplace)


@router.callback_query(StateFilter(FSMService.workplace))
async def get_login_aurhorize(callback: Message, state: FSMContext, bot: Bot):
    selected_city = callback.data
    await state.update_data(city=selected_city)

    await callback.message.edit_text('Выберите цех 👇',
                                     reply_markup=await get_now_workshop_ikb())
    await state.set_state(FSMService.app)


@router.callback_query(StateFilter(FSMService.app))
async def get_app(callback: Message, state: FSMContext, bot: Bot):
    selected_workspace = callback.data
    await state.update_data(workspace=selected_workspace)
    user_data = await state.get_data()
    selected_city = user_data.get('city')
    selected_workspace = user_data.get('workspace')

    await callback.message.answer(f'Город: <b>{selected_city}</b>\n'
                                  f'Цех: <b>{selected_workspace}</b>\n'
                                  f'Выберите продукты в приложении 👇',
                                  reply_markup=await get_web_app(selected_city, selected_workspace,
                                                                 callback.from_user.id))






