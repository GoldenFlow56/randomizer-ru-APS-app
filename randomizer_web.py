import streamlit as st
import random
import pandas as pd
from io import BytesIO

# Минимальный CSS
st.markdown("""
<style>
    body {
        background-color: #f0f2f6;
        font-family: 'Arial', sans-serif;
    }
    h1 {
        color: #1e90ff;
        text-align: center;
        font-size: 2em;
    }
    .stButton>button {
        background-color: #1e90ff;
        color: white;
        border-radius: 5px;
        padding: 8px 16px;
        font-size: 1em;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Списки данных
male_names = ['Александр', 'Андрей', 'Дмитрий', 'Иван', 'Максим', 'Сергей']
female_names = ['Анна', 'Мария', 'Ольга', 'Елена', 'Наталья', 'Татьяна']
surnames = ['Иванов', 'Петров', 'Смирнов', 'Кузнецов', 'Попов', 'Васильев']
cities = ['Москва', 'Санкт-Петербург', 'Новосибирск', 'Екатеринбург', 'Казань', 'Красноярск']
streets = ['Центральная', 'Молодёжная', 'Школьная', 'Лесная', 'Садовая', 'Новая']
mobile_prefixes = ['910', '911', '912', '913', '914', '915', '916', '917', '918', '919']

def generate_random_data():
    is_female = random.choice([True, False])
    name = random.choice(female_names if is_female else male_names)
    surname = random.choice(surnames)
    if is_female and surname[-1] not in 'ие':
        surname += 'а'
    city = random.choice(cities)
    street = random.choice(streets)
    house = random.randint(1, 200)
    apartment = random.randint(1, 100)
    postal_code = random.randint(100000, 999999)
    phone = f"+7 ({random.choice(mobile_prefixes)}) {random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(10, 99)}"
    return {
        'Имя': f"{name} {surname}",
        'Город': city,
        'Улица': f"ул. {street}, д. {house}, кв. {apartment}",
        'Индекс': postal_code,
        'Телефон': phone
    }

# Интерфейс
st.title("Генератор профилей App Store")
st.write("Создайте реалистичные данные для тестирования приложений")

if 'profiles' not in st.session_state:
    st.session_state.profiles = []

with st.container():
    col1, col2, col3 = st.columns(3)
    with col1:
        num_profiles = st.number_input("Количество профилей:", min_value=1, value=5, step=1)
    with col2:
        if st.button("Сгенерировать", type="primary"):
            new_profiles = [generate_random_data() for _ in range(num_profiles)]
            st.session_state.profiles.extend(new_profiles)
    with col3:
        if st.button("Очистить"):
            st.session_state.profiles = []

    if st.session_state.profiles:
        df = pd.DataFrame(st.session_state.profiles)
        st.dataframe(df, use_container_width=True, hide_index=True)

        # Экспорт в XLSX
        buffer = BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Профили')
        buffer.seek(0)

        st.download_button(
            label="Скачать как XLSX",
            data=buffer,
            file_name="profiles.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary"
        )
    else:
        st.info("Сначала сгенерируйте профили")
