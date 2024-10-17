import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pydeck as pdk

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
    plt.style.use('ggplot')  # Используем стиль ggplot, который встроен в Matplotlib

    # Линейный график
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

    # Отображаем линейный график в Streamlit
    st.pyplot(plt)

    # Столбчатая диаграмма
    plt.figure(figsize=(12, 6))
    sns.barplot(data=filtered_data, x='year', y='F_mod_sev_tot', hue='Страна', ci=None)
    
    # Настройка осей
    plt.title('Сравнение модифицированной тяжести продовольственной безопасности по странам', fontsize=16, weight='bold', color='darkblue')
    plt.xlabel('Год', fontsize=12, color='darkgreen')
    plt.ylabel('Модерированная тяжесть продовольственной безопасности', fontsize=12, color='darkgreen')
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=10)
    plt.legend(title='Страна', fontsize=10, title_fontsize=12, loc='upper right')

    # Отображаем столбчатую диаграмму в Streamlit
    st.pyplot(plt)

    # Интерактивные пояснения
    with st.expander("Интерактивные пояснения"):
        st.write("""
            Модифицированная тяжесть продовольственной безопасности (F_mod_sev_tot) измеряет уровень
            продовольственной безопасности для населения. На графиках вы можете увидеть изменения 
            этого показателя по странам и годам. Столбчатая диаграмма позволяет сравнить показатели 
            между странами за выбранные годы.
        """)

    # Карта
    st.write("Карта с расположением стран:")
    map_data = pd.DataFrame({
        'Страна': ['Казахстан', 'Кыргызстан', 'Таджикистан', 'Узбекистан'],
        'Лат': [48.0196, 41.2044, 38.8610, 41.3775],
        'Лон': [66.9237, 74.7661, 74.5698, 64.5850]
    })

    # Добавляем карту
    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(
            latitude=39.5,
            longitude=66.9,
            zoom=3,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=map_data,
                get_position='[Лон, Лат]',
                get_color='[255, 0, 0]',
                get_radius=50000,
            ),
        ],
    ))
else:
    st.error("Не удалось получить данные для выбранных стран.")
