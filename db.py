import pandas as pd
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
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
DATABASE_URI = 'postgresql://calls_owner:g0Z2omVMykvS@ep-calm-bar-a26gvvaw.eu-central-1.aws.neon.tech/products'
engine = create_engine(DATABASE_URI, echo=True)
SessionLocal = sessionmaker(bind=engine)

def create_table_products():
    """Создает таблицу в базе данных."""
    Base.metadata.create_all(engine)
    print('Таблица создана')


def create_table_from_csv():
    """Загружает список продуктов из CSV в базу данных."""
    df = pd.read_csv('products.csv')
    with engine.begin() as conn:
        df.to_sql('products_list', con=conn, if_exists='replace', index=False, method='multi')
    print('Список продуктов загружен в базу')


def insert_data(data: tuple):
    """Вставляет данные в таблицу."""

    count_print = data[6]

    with SessionLocal() as session:
        new_product = Product(
            user_id=data[0],
            city=data[1],
            workshop=data[2],
            product_name=data[3],
            time_start=data[4],
            time_end=data[5]
        )

        for i in range(count_print):
            session.add(new_product)
        session.commit()
    print("Данные вставлены.")


def get_product_names():
    """Получает имена продуктов из CSV."""
    df = pd.read_csv('products.csv')
    return df