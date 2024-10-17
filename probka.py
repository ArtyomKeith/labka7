import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Загружаем данные
file_path = "aggregated_results.xlsx"  # Укажите путь к вашему файлу
df_pandas = pd.read_excel(file_path)

# Разделяем 'year' на страну и год
df_pandas[['country', 'year']] = df_pandas['year'].str.split('_', expand=True)

# Преобразуем год в числовой формат
df_pandas['year'] = pd.to_numeric(df_pandas['year'])

# Словарь для замены стран на русские названия
country_mapping = {
    'Kazakhstan': 'Казахстан',
    'KGZ': 'Кыргызстан',
    'TAIJ': 'Таджикистан',
    'UZB': 'Узбекистан'
}

# Заменяем названия стран в столбце 'country'
df_pandas['country'] = df_pandas['country'].replace(country_mapping)

# Переименовываем столбец 'country' на 'Страна'
df_pandas = df_pandas.rename(columns={'country': 'Страна'})

# Вывод информации о данных
st.write("### Информация о данных")
st.write(f"Количество записей: {len(df_pandas)}")
st.write("Столбцы данных:")
st.write(df_pandas.columns.tolist())

# Выбор стран для отображения
countries = df_pandas['Страна'].unique().tolist()
selected_countries = st.multiselect("Выберите страны для отображения:", countries, default=countries)

# Слайдер для выбора диапазона лет
year_range = st.slider("Выберите диапазон лет:", min_value=int(df_pandas['year'].min()), 
                        max_value=int(df_pandas['year'].max()), value=(2014, 2017))

# Фильтруем данные по выбранным странам и диапазону лет
filtered_data = df_pandas[(df_pandas['Страна'].isin(selected_countries)) & 
                           (df_pandas['year'].between(year_range[0], year_range[1]))]

# Проверка, что данные не пустые после фильтрации
if not filtered_data.empty:
    # Добавляем текстовое описание
    st.write("График ниже показывает изменение модифицированной тяжести продовольственной безопасности по годам для выбранных стран.")

    # Настройка стиля
    plt.style.use('ggplot')  # Используем стиль ggplot

    # Настройка графика
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=filtered_data, x='year', y='F_mod_sev_tot', hue='Страна', marker='o', linewidth=2.5)

    # Настройка осей
    plt.xticks(filtered_data['year'].unique(), rotation=45, fontsize=10)
    plt.yticks(fontsize=10)

    # Добавляем заголовок и подписи к осям
    plt.title('Изменение продовольственной безопасности по годам', fontsize=16, weight='bold', color='darkblue')
    plt.xlabel('Год', fontsize=12, color='darkgreen')
    plt.ylabel('Модерированная тяжесть продовольственной безопасности', fontsize=12, color='darkgreen')

    # Настройка легенды
    plt.legend(title='Страна', fontsize=10, title_fontsize=12, loc='upper right')

    # Добавляем сетку
    plt.grid(True, which='both', linestyle='--', linewidth=0.7, color='gray', alpha=0.7)

    # Добавляем подгонку макета
    plt.tight_layout()

    # Отображаем график в Streamlit
    st.pyplot(plt)

    # График распределения значений модифицированной тяжести
    plt.figure(figsize=(12, 6))
    sns.histplot(filtered_data['F_mod_sev_tot'], bins=20, kde=True, color='orange')
    plt.title('Распределение модифицированной тяжести продовольственной безопасности', fontsize=16)
    plt.xlabel('Модерированная тяжесть', fontsize=12)
    plt.ylabel('Частота', fontsize=12)
    st.pyplot(plt)

    # Кнопка для загрузки данных
    st.download_button(
        label="Скачать данные в формате CSV",
        data=filtered_data.to_csv(index=False).encode('utf-8'),
        file_name='filtered_data.csv',
        mime='text/csv',
    )

else:
    st.error("Не удалось получить данные для выбранных стран.")

# Кнопка сброса фильтров
if st.button("Сбросить фильтры"):
    st.session_state.selected_countries = countries
    st.session_state.year_range = (2014, 2017)
    st.experimental_rerun()  # Перезапускаем скрипт, чтобы применить изменения
