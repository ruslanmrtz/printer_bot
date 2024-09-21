import streamlit as st
from datetime import datetime, timedelta

from print_check.printer import printer_check
import db

# Проверка инициализации базы данных
if 'db_initialized' not in st.session_state:
    db.create_table_products()
    db.create_table_from_csv()
    st.session_state.db_initialized = True


# Получаем параметры из URL
query_params = st.query_params
city = query_params.get("city", "").replace('%20', ' ')
workspace = query_params.get("workspace", "").replace('%20', ' ')
user_id = query_params.get("user_id", "")

st.markdown(f'### Вы выбрали:')
st.markdown(f'**Город:** {city}')
st.markdown(f'**Цех:** {workspace}')

# Поле для ввода поискового запроса
df = db.get_product_names()
options = sorted(([""] + list(df['Продукт'])))
search_query = st.text_input("Поиск ингредиента")

filtered_options = [opt for opt in options if search_query.lower() in opt.lower()]
selected_option = st.selectbox("Выберите ингредиент", filtered_options)

if st.button("Печатать", key="print_button"):
    if selected_option:
        st.success('Успешно!')

        hours = int(df[df['Продукт'] == selected_option]['Часы'].iloc[0])

        time_start = datetime.now()
        time_end = time_start + timedelta(hours=hours)

        data = (user_id, city, workspace, selected_option, time_start, time_end)
        db.insert_data(data)

        printer_check(25, selected_option, user_id)
    else:
        st.error("Пожалуйста, выберите ингредиент!")