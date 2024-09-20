import streamlit as st


# Получаем параметры из URL
query_params = st.query_params
city = query_params.get("city", [""])
workspace = query_params.get("workspace", [""])


st.markdown(f'### Вы выбрали:')
st.markdown(f'**Город:** {city}')
st.markdown(f'**Цех:** {workspace}')

# Поле для ввода поискового запроса
option = st.selectbox(
    "Выберите ингредиент",
    ("", "Лук", "Сосиска", "Рис"),
)

if st.button("Печатать", key="print_button"):
    if option:
        st.success('Успешно!')
    else:
        st.error("Пожалуйста, выберите ингредиент!")