import streamlit as st

from print_check.printer import printer_check

# Получаем параметры из URL
query_params = st.query_params
city = query_params.get("city", "").replace('%20', ' ')
workspace = query_params.get("workspace", "").replace('%20', ' ')
user_id = query_params.get("user_id", "")

st.markdown(f'### Вы выбрали:')
st.markdown(f'**Город:** {city}')
st.markdown(f'**Цех:** {workspace}')

# Поле для ввода поискового запроса
options = ["", "Лук", "Сосиска", "Рис", "Морковь"]
search_query = st.text_input("Поиск ингредиента")

filtered_options = [opt for opt in options if search_query.lower() in opt.lower()]
selected_option = st.selectbox("Выберите ингредиент", filtered_options)

if st.button("Печатать", key="print_button"):
    if selected_option:
        st.success('Успешно!')

        printer_check(25, selected_option, user_id)
    else:
        st.error("Пожалуйста, выберите ингредиент!")