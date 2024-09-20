import streamlit as st


# Получаем параметры из URL
query_params = st.query_params
city = query_params.get("city", [""])
workspace = query_params.get("workspace", [""])


st.markdown(f'### Вы выбрали:')
st.markdown(f'**Город:** {city}')
st.markdown(f'**Цех:** {workspace}')

# Поле для ввода поискового запроса
options = ["", "Лук", "Сосиска", "Рис", "Морковь"]
search_query = st.text_input("Поиск ингредиента")

filtered_options = [opt for opt in options if search_query.lower() in opt.lower()]
selected_option = st.selectbox("Выберите ингредиент", filtered_options)

if st.button("Печатать", key="print_button"):
    if option:
        st.success('Успешно!')
    else:
        st.error("Пожалуйста, выберите ингредиент!")