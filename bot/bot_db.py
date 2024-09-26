from sqlalchemy import Column, Integer, String, DateTime, text, ARRAY
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Определяем базовый класс для модели
Base = declarative_base()


# Определяем модель таблицы Products
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String)  # Изменил на String, чтобы соответствовать твоему коду
    city = Column(String)
    workshop = Column(String)
    product_name = Column(String)
    time_start = Column(DateTime)
    time_end = Column(DateTime)


class Cities(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city = Column(String, nullable=False)
    workshop = Column(String)  # Адрес может быть None
    chef = Column(String, nullable=False)
    phones = Column(ARRAY(String), nullable=False)  # Используем ARRAY для хранения списка телефонов


# Определяем модель таблицы Users
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    phone = Column(String, unique=True, nullable=False)
    user_id = Column(String, unique=True, nullable=False)


# Создание подключения к базе данных
DATABASE_URI = 'postgresql+asyncpg://calls_owner:g0Z2omVMykvS@ep-calm-bar-a26gvvaw.eu-central-1.aws.neon.tech/products'
engine = create_async_engine(DATABASE_URI)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_city_phones(city_name, workshop=None):
    async with AsyncSessionLocal() as session:
        # Создаем начальный запрос для получения телефонов из таблицы cities
        query = text("SELECT phones FROM cities WHERE city = :city_name")

        # Если workshop предоставлен, добавляем его к запросу
        if workshop:
            query = text("SELECT phones FROM cities WHERE city = :city_name AND workshop = :workshop")

        # Выполняем запрос для получения телефонов
        result_cities = await session.execute(query, {'city_name': city_name, 'workshop': workshop})
        city_phones = result_cities.scalar_one_or_none()

        l = city_phones[1:-1].split(',')
        return l


# Функция для добавления пользователя в базу данных
async def add_user(phone, user_id):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            await session.execute(
                text("INSERT INTO users (phone, user_id) VALUES (:phone, :user_id) "
                     "ON CONFLICT (phone) DO NOTHING"),
                {'phone': phone, 'user_id': user_id}
            )
        await session.commit()


async def get_user_id_by_phone(phone):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            text("SELECT user_id FROM users WHERE phone = :phone"),
            {'phone': phone}
        )
        return result.scalar_one_or_none()


# Функция для получения всех пользователей
async def get_all_users():
    async with AsyncSessionLocal() as session:
        result = await session.execute("SELECT * FROM users")
        users = result.fetchall()
        return users


# Функция для создания таблиц
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)