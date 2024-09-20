from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


async def get_city_ikb(cities: list) -> InlineKeyboardMarkup:
    buttons = []
    for city in cities:
        city_button = [InlineKeyboardButton(text=city, callback_data=city)]

        buttons.append(city_button)

    cancel = InlineKeyboardButton(text="Назад 🔙",
                                  callback_data=f'main_menu_return')

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[*buttons, [cancel]]
    )

    return keyboard


async def get_now_workshop_ikb() -> InlineKeyboardMarkup:
    workshop1 = InlineKeyboardButton(text="Пролетарский просп., 10/3",
                                 callback_data=f'Пролетарский просп., 10/3')
    workshop2 = InlineKeyboardButton(text="ул. Есенина, 4",
                                     callback_data=f'ул. Есенина, 4')
    workshop3 = InlineKeyboardButton(text="Набережный просп., 10/1",
                                     callback_data=f'Набережный просп., 10/1')

    cancel = InlineKeyboardButton(text="Назад 🔙",
                                  callback_data=f'_city')

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[workshop1], [workshop2], [workshop3], [cancel]]
    )

    return keyboard


async def get_web_app(city: str, workspace: str, id: int):
    app = (
        InlineKeyboardButton(text="Открыть выбор",
                             web_app=WebAppInfo(
                              url=f'https://printerbot.streamlit.app/?city={city}&workspace={workspace}&user_id={id}')))

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[app]]
    )

    return keyboard