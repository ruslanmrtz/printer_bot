import streamlit as st


# Поле для ввода поискового запроса
option = st.selectbox(
    "Выберите ингредиент",
    ("", "Лук", "Сосиска", "Рис"),
)

if st.button("Печатать"):
    if option:
        st.success('Успешно!')
    else:
        st.error("Пожалуйста, выберите ингредиент!")