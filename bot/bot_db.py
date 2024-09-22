import pandas as pd
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker


# Определяем базовый класс для модели
Base = declarative_base()


# Определяем модель таблицы
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String)  # изменил на String, чтобы соответствовать твоему коду
    city = Column(String)
    workshop = Column(String)
    product_name = Column(String)
    time_start = Column(DateTime)
    time_end = Column(DateTime)


# Создание подключения к базе данных
DATABASE_URI = 'postgresql+asyncpg://calls_owner:g0Z2omVMykvS@ep-calm-bar-a26gvvaw.eu-central-1.aws.neon.tech/products'
engine = create_async_engine(DATABASE_URI, echo=True)
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)

