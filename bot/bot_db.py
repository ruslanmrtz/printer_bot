from sqlalchemy import Column, Integer, String, DateTime, text, ARRAY
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Определяем базовый класс для модели
Base = declarative_base()


# Определяем модель таблицы Products
# Определяем модель таблицы Products
class Product(Base):
    __tablename__ = 'printer_products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(50))  # Указали длину
    city = Column(String(100))  # Указали длину
    workshop = Column(String(100))  # Указали длину
    product_name = Column(String(100))  # Указали длину
    time_start = Column(DateTime)
    time_end = Column(DateTime)

class Cities(Base):
    __tablename__ = 'printer_cities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String(100), nullable=False)  # Указали длину
    workshop = Column(String(100))  # Указали длину
    chef = Column(String(100), nullable=False)  # Указали длину
    phones = Column(String(100), nullable=False)  # Строка, содержащая номера телефонов, разделенные запятыми

# Определяем модель таблицы Users
class User(Base):
    __tablename__ = 'printer_users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column(String(15), unique=True, nullable=False)  # Указали длину
    user_id = Column(String(50), unique=True, nullable=False)  # Указали длину


# Создание подключения к базе данных
DATABASE_URI = 'mysql+aiomysql://root:nLplQtuG@82.202.177.215/samurai_db'
engine = create_async_engine(DATABASE_URI)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_city_phones(city_name, workshop=None):
    async with AsyncSessionLocal() as session:
        # Создаем начальный запрос для получения телефонов из таблицы cities
        query = text("SELECT phones FROM printer_cities WHERE city = :city_name")

        # Если workshop предоставлен, добавляем его к запросу
        if workshop:
            query = text("SELECT phones FROM cities WHERE printer_city = :city_name AND workshop = :workshop")

        # Выполняем запрос для получения телефонов
        result_cities = await session.execute(query, {'city_name': city_name, 'workshop': workshop})
        city_phones = result_cities.scalar_one_or_none()

        l = city_phones.split(',')
        return l


# Функция для добавления пользователя в базу данных
async def add_user(phone, user_id):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            await session.execute(
                text("INSERT IGNORE INTO printer_users (phone, user_id) VALUES (:phone, :user_id)"),
                {"phone": phone, "user_id": user_id}  # Используем словарь для именованных параметров
            )
        await session.commit()


async def get_user_id_by_phone(phone):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            text("SELECT user_id FROM printer_users WHERE phone = :phone"),
            {'phone': phone}
        )
        return result.scalar_one_or_none()


# Функция для получения всех пользователей
async def get_all_users():
    async with AsyncSessionLocal() as session:
        result = await session.execute("SELECT * FROM printer_users")
        users = result.fetchall()
        return users


# Функция для создания таблиц
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)