from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from cities import get_cities, get_workshop

async def get_city_ikb() -> InlineKeyboardMarkup:
    cities = await get_cities()

    buttons = []
    for city in cities:
        city_button = [InlineKeyboardButton(text=city, callback_data=city)]

        buttons.append(city_button)

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[*buttons]
    )

    return keyboard


async def get_now_workshop_ikb() -> InlineKeyboardMarkup:

    workshops = await get_workshop()

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
                              url=f'https://printerbot-ssamurai.ru/?city={city}&workspace={workspace}&user_id={id}')))

    cancel_city = InlineKeyboardButton(text="К выбору города 🔙",
                                            callback_data=f'city')

    # cancel_workshop = InlineKeyboardButton(text="К выбору цеха 🔙",
    #                                    callback_data=f'workshop')

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[app], [cancel_city]]
    )

    return keyboard