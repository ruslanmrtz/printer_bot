import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, DateTime
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
DATABASE_URI = 'postgresql+psycopg2://calls_owner:g0Z2omVMykvS@ep-calm-bar-a26gvvaw.eu-central-1.aws.neon.tech/products'
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)


def create_table_products():
    # Создаем таблицы в базе данных
    Base.metadata.create_all(engine)
    print('Таблица создана')


def create_table_from_csv():
    df = pd.read_csv('products.csv')
    df.to_sql('products_list', con=engine, if_exists='replace', index=False)
    print('Список продуктов загружен в базу')


def insert_data(data: tuple):
    """Вставляет данные в таблицу."""
    session = Session()
    new_product = Product(
        user_id=data[0],
        city=data[1],
        workshop=data[2],
        product_name=data[3],
        time_start=data[4],
        time_end=data[5]
    )

    session.add(new_product)
    session.commit()
    session.close()
    print("Данные вставлены.")


def get_product_names():
    df = pd.read_csv('products.csv')

    return df


