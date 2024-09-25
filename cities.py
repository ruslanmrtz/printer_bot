import pandas as pd
import time


st_time = time.time()
cities = {'Сургут':
              {'Пролетарский 10/3': ('Исматов Ш.М', [89229992999, 89003864646, 89825199119, 89923570076]),
                'Есенина 4': ("Умаров М.М", [89229992999, 89003864646, 89825199119, 79224261236]),
                'Набережный 10/3': ('Джураев Д.М', [89229992999, 89003864646, 89825199119, 89048830975])},
          'Нефтеюганск': ('Кадырбеков Д.Т', [89229992999, 89003864646,  89825199119, 89227779230]),
          'Федоровский': ('Павленко В.В', [89824041536, 89505055979, 79224055219]),
          'Ханты-Мансийск': ('Самарцев В.А', [79828879868]),
          'Лянтор': ('Шаропова М.И', [89224230007, 79224230007]),
          'Когалым': ('Бувачалов О.', [79824197004, 79824197004]),
          'Пыть-Ях': ('Исматов Ш.М', [89229992999, 89003864646, 89825199119])
          }

data = []
for city, info in cities.items():
    if isinstance(info, dict):  # если это Сургут с несколькими адресами
        for address, (person, phones) in info.items():
            data.append([city, address, person, phones])
    else:
        person, phones = info
        data.append([city, None, person, phones])

# Создание DataFrame
df = pd.DataFrame(data, columns=['Город', 'Цех', 'СтаршийПовар', 'Телефоны'])


def get_df_cities() -> pd.DataFrame:
    data = []
    for city, inf in cities.items():
        if isinstance(inf, dict):  # если это Сургут с несколькими адресами
            for address, (person, phones) in inf.items():
                data.append([city, address, person, phones])
        else:
            person, phones = inf
            data.append([city, None, person, phones])

    # Создание DataFrame
    df = pd.DataFrame(data, columns=['city', 'workshop', 'chef', 'phones'])

    return df



async def get_cities():
    return cities.keys()


async def get_workshop():
    return cities['Сургут'].keys()
