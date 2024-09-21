from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo


async def get_city_ikb(cities: list) -> InlineKeyboardMarkup:
    buttons = []
    for city in cities:
        city_button = [InlineKeyboardButton(text=city, callback_data=city)]

        buttons.append(city_button)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[*buttons]
    )

    return keyboard


async def get_now_workshop_ikb(workshops: list) -> InlineKeyboardMarkup:

    buttons = []
    for ws in workshops:
        workshop = [InlineKeyboardButton(text=ws, callback_data=ws)]
        buttons.append(workshop)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[*buttons]
    )

    return keyboard


async def get_web_app(city: str, workspace: str, id: int):
    app = (
        InlineKeyboardButton(text="Открыть выбор",
                             web_app=WebAppInfo(
                              url=f'https://243f-2a01-540-a617-b300-3964-5f7c-b4ca-2d68.ngrok-free.app/?city={city}&workspace={workspace}&user_id={id}')))

    cancel_city = InlineKeyboardButton(text="К выбору города 🔙",
                                  callback_data=f'city')

    cancel_workshop = InlineKeyboardButton(text="К выбору цеха 🔙",
                                       callback_data=f'workshop')

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[app], [cancel_city], [cancel_workshop]]
    )

    return keyboard