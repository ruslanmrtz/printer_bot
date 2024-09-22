import streamlit as st
from datetime import datetime, timedelta

from print_check.to_pdf import crop_and_display_pdf
from print_check.printer import printer_check, get_pdf
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


# Создаем пустое пространство для отображения PDF
pdf_placeholder = st.empty()


if 'check_check' in st.session_state:
    pdf_file = f'print_check/checks/check_{user_id}.pdf'
    cropped_image = crop_and_display_pdf(pdf_file, 140, 110, 375, 200)
    pdf_placeholder.image(cropped_image)
    del st.session_state.check_check


# Отображение уведомления об успешной операции, если оно есть
if 'success_message' in st.session_state:
    st.success(st.session_state.success_message)
    del st.session_state.success_message  # Удаляем сообщение после отображения

st.markdown(f'**Город:** {city}')
st.markdown(f'**Цех:** {workspace}')

# Поле для ввода поискового запроса
df = db.get_product_names()
options = sorted(([""] + list(df['Продукт'])))
search_query = st.text_input("Поиск ингредиента")

filtered_options = [opt for opt in options if search_query.lower() in opt.lower()]
selected_option = st.selectbox("Выберите ингредиент", filtered_options)

check_button = st.button("Открыть этикетку")
print_button = st.button("Печатать этикетки", key="print_button")

if print_button:
    if selected_option:

        hours = int(df[df['Продукт'] == selected_option]['Часы'].iloc[0])

        time_start = datetime.now()
        time_end = time_start + timedelta(hours=hours)

        printer_check(hours, selected_option, user_id, time_start, time_end)

        data = (user_id, city, workspace, selected_option, time_start, time_end)
        db.insert_data(data)

        # printer_check(25, selected_option, user_id)

        # Уведомление об успешной операции
        st.session_state.success_message = 'Успешная печать'  # Сохраняем сообщение в состоянии сессии
        st.rerun()  # Перезапускаем приложение, чтобы отобразить уведомление

    else:
        st.error("Пожалуйста, выберите ингредиент!")


if check_button:
    if selected_option:
        hours = int(df[df['Продукт'] == selected_option]['Часы'].iloc[0])

        time_start = datetime.now()
        time_end = time_start + timedelta(hours=hours)

        get_pdf(hours, selected_option, user_id, time_start, time_end)

        # Уведомление об успешной операции
        st.session_state.check_check = 'Проверить'  # Сохраняем сообщение в состоянии сессии
        st.rerun()  # Перезапускаем приложение, чтобы отобразить уведомление

    else:
        st.error("Пожалуйста, выберите ингредиент!")