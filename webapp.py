import streamlit as st
from datetime import datetime, timedelta

from print_check.to_pdf import crop_and_display_pdf, get_pdf
from print_check.printer import printer_check
import db

# Проверка инициализации базы данных
if 'db_initialized' not in st.session_state:
    db.create_table_products()
    db.create_city()
    db.create_table_from_csv()
    st.session_state.db_initialized = True

# Получаем параметры из URL
query_params = st.query_params
city = query_params.get("city", "").replace('%20', ' ')
workspace = query_params.get("workspace", "").replace('%20', ' ')
user_id = query_params.get("user_id", "")

chef = db.get_chef(city, workspace)

# Создаем пустое пространство для отображения PDF
pdf_placeholder = st.empty()

# Отображение уведомления об успешной операции, если оно есть
if 'success_message' in st.session_state:
    st.success(st.session_state.success_message)
    del st.session_state.success_message  # Удаляем сообщение после отображения

st.markdown(f'**Город:** {city}')
if workspace:
    st.markdown(f'**Цех:** {workspace}')

# Поле для ввода поискового запроса
df = db.get_product_names()
options = sorted(([""] + df['Продукт'].to_list()))

selected_option = st.selectbox("Выберите ингредиент", options)

print_count = st.number_input('Количество этикеток', min_value=1, step=1, value=1)

# Проверяем, изменился ли выбранный ингредиент
if 'previous_option' not in st.session_state:
    st.session_state.previous_option = selected_option
elif st.session_state.previous_option != selected_option:
    # Если продукт изменился, сбрасываем флаги
    st.session_state.pdf_generated = False
    st.session_state.previous_option = selected_option

print_button = st.button("Печатать этикетки", key="print_button")

if print_button:
    if selected_option:
        hours = int(df[df['Продукт'] == selected_option]['Часы'].iloc[0])
        time_start = datetime.now()
        time_end = time_start + timedelta(hours=hours)

        get_pdf(hours, selected_option, user_id,
                time_start, time_end, chef, city, workspace)

        # printer_check(print_count, user_id)

        data = (user_id, city, workspace, selected_option, time_start, time_end, print_count)
        db.insert_data(data)

        # Уведомление об успешной операции
        st.session_state.success_message = 'Успешная печать!'
        st.session_state.pdf_generated = True  # Устанавливаем, что PDF сгенерирован
        st.rerun()  # Перезапускаем приложение, чтобы отобразить уведомление
    else:
        st.error("Пожалуйста, выберите ингредиент!")

# Генерация PDF для выбранного продукта
if selected_option:
    if 'pdf_generated' not in st.session_state or not st.session_state.pdf_generated:
        hours = int(df[df['Продукт'] == selected_option]['Часы'].iloc[0])
        time_start = datetime.now()
        time_end = time_start + timedelta(hours=hours)

        get_pdf(hours, selected_option, user_id, time_start,
                time_end, chef,  city, workspace, show=True)

        # Уведомление об успешной операции
        st.session_state.check_check = 'Проверить'
        st.session_state.pdf_generated = True  # Отмечаем, что PDF уже был сгенерирован
        st.rerun()

# Проверяем и отображаем PDF, если он уже был сгенерирован
if 'pdf_generated' in st.session_state and st.session_state.pdf_generated:
    pdf_file = f'print_check/checks/check_{user_id}.pdf'
    cropped_image = crop_and_display_pdf(pdf_file, left=2, top=2, right=460, bottom=315)
    pdf_placeholder.image(cropped_image, width=200)

# Проверяем и отображаем PDF, если есть флаг check_check
if 'check_check' in st.session_state:
    pdf_file = f'print_check/checks/check_{user_id}.pdf'
    cropped_image = crop_and_display_pdf(pdf_file, left=2, top=2, right=460, bottom=315)
    pdf_placeholder.image(cropped_image, width=200)
    del st.session_state.check_check
