import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pydeck as pdk

# Загружаем данные через интерфейс
uploaded_file = st.file_uploader("Загрузите файл Excel", type="xlsx")
if uploaded_file:
    df_pandas = pd.read_excel(uploaded_file)
else:
    st.stop()

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

# Словарь для показателей и их русских названий
metrics_mapping = {
    'F_mod_sev_ad': 'Модиф. тяжесть прод. безоп. среди взросл.',
    'F_sev_ad': 'Тяжесть прод. безоп. среди взросл.',
    'F_mod_sev_child': 'Модиф. тяжесть прод. безоп. среди детей',
    'F_sev_child': 'Тяжесть прод. безоп. среди детей',
    'F_mod_sev_tot': 'Общая модифиц. тяжесть прод. безоп.',
    'F_sev_tot': 'Общая тяжесть прод. безоп.'
}

# Выбор показателя
metrics = list(metrics_mapping.keys())
selected_metric = st.selectbox("Выберите показатель для визуализации:", metrics, format_func=lambda x: metrics_mapping[x])

# Фильтруем данные по выбранным странам и диапазону лет
filtered_data = df_pandas[(df_pandas['Страна'].isin(selected_countries)) & 
                           (df_pandas['year'].between(year_range[0], year_range[1]))]

# Проверка, что данные не пустые после фильтрации
if not filtered_data.empty:
    # Статистика
    st.write("Статистика по выбранным данным:")
    stats = filtered_data.groupby('Страна')[selected_metric].agg(['mean', 'min', 'max']).reset_index()
    stats.columns = ['Страна', 'Среднее', 'Минимум', 'Максимум']  # Русские названия столбцов
    st.write(stats)

    # Таблица с данными по выбранному показателю
    st.dataframe(filtered_data[['Страна', 'year', selected_metric]])

    # Настройка стиля
    plt.style.use('ggplot')

    # Вкладки для графиков
    tab1, tab2 = st.tabs(["Линейный график", "Столбчатая диаграмма"])

    # Линейный график
    with tab1:
        st.write(f"График изменения {metrics_mapping[selected_metric]} по годам.")
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=filtered_data, x='year', y=selected_metric, hue='Страна', marker='o', linewidth=2.5)

        plt.title(f'Изменение {metrics_mapping[selected_metric]} по годам', fontsize=16, weight='bold', color='darkblue')
        plt.xlabel('Год', fontsize=12, color='darkgreen')
        plt.ylabel(metrics_mapping[selected_metric], fontsize=12, color='darkgreen')
        plt.grid(True, linestyle='--', linewidth=0.7, color='gray', alpha=0.7)
        plt.tight_layout()
        st.pyplot(plt)

    # Столбчатая диаграмма
    with tab2:
        st.write(f"Сравнение {metrics_mapping[selected_metric]} по странам.")
        plt.figure(figsize=(12, 6))
        sns.barplot(data=filtered_data, x='year', y=selected_metric, hue='Страна', ci=None)

        plt.title(f'Сравнение {metrics_mapping[selected_metric]} по странам', fontsize=16, weight='bold', color='darkblue')
        plt.xlabel('Год', fontsize=12, color='darkgreen')
        plt.ylabel(metrics_mapping[selected_metric], fontsize=12, color='darkgreen')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(plt)

    # Карта с расположением стран
    st.write("Интерактивная карта:")
    map_data = pd.DataFrame({
        'Страна': ['Казахстан', 'Кыргызстан', 'Таджикистан', 'Узбекистан'],
        'Лат': [48.0196, 41.2044, 38.8610, 41.3775],
        'Лон': [66.9237, 74.7661, 74.5698, 64.5850]
    })

    st.pydeck_chart(pdk.Deck(
        initial_view_state=pdk.ViewState(latitude=39.5, longitude=66.9, zoom=3),
        layers=[
            pdk.Layer(
                'ScatterplotLayer',
                data=map_data,
                get_position='[Лон, Лат]',
                get_color='[200, 30, 0, 160]',
                get_radius=50000,
                pickable=True,
            ),
        ],
        tooltip={"text": "{Страна}\nКоординаты: [{Лат}, {Лон}]"}
    ))

    # Интерактивные пояснения
    with st.expander("Интерактивные пояснения"):
        st.write(f"Этот график показывает изменения {metrics_mapping[selected_metric]} по странам и годам. Вы можете "
                 f"видеть детализированную информацию, выбирая разные страны и годы.")
else:
    st.error("Не удалось получить данные для выбранных стран.")
