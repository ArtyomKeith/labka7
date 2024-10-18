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

# Словарь для показателей и их русских названий
metrics_mapping = {
    'F_mod_sev_ad': 'Модиф. тяжесть прод. безоп. среди взросл.',
    'F_sev_ad': 'Тяжесть прод. безоп. среди взросл.',
    'F_mod_sev_child': 'Модиф. тяжесть прод. безоп. среди детей',
    'F_sev_child': 'Тяжесть прод. безоп. среди детей',
    'F_mod_sev_tot': 'Общая модифиц. тяжесть прод. безоп.',
    'F_sev_tot': 'Общая тяжесть прод. безоп.',
    'F_very_sev_ad': 'Очень тяжелая прод. безоп. среди взросл.',
    'F_very_sev_child': 'Очень тяжелая прод. безоп. среди детей'  # Новый показатель
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

    # Экспорт данных
    st.download_button(
        label="Экспортировать данные в CSV",
        data=stats.to_csv(index=False).encode('utf-8'),
        file_name='stats.csv',
        mime='text/csv'
    )
    st.download_button(
        label="Экспортировать данные в Excel",
        data=stats.to_excel(index=False, engine='openpyxl'),
        file_name='stats.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    # Настройка стиля
    plt.style.use('ggplot')  # Используем стиль ggplot, который встроен в Matplotlib

    # Вкладки для графиков
    tab1, tab2 = st.tabs(["Линейный график", "Столбчатая диаграмма"])

    # Линейный график
    with tab1:
        st.write("График ниже показывает изменение {} по годам для выбранных стран.".format(metrics_mapping[selected_metric]))
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=filtered_data, x='year', y=selected_metric, hue='Страна', marker='o', linewidth=2.5)

        # Настройка осей
        plt.xticks(filtered_data['year'].unique(), rotation=45, fontsize=10)
        plt.yticks(fontsize=10)

        # Добавляем заголовок и подписи к осям
        plt.title('Изменение {} по годам'.format(metrics_mapping[selected_metric]), fontsize=16, weight='bold', color='darkblue')
        plt.xlabel('Год', fontsize=12, color='darkgreen')
        plt.ylabel(metrics_mapping[selected_metric], fontsize=12, color='darkgreen')

        # Настройка легенды
        plt.legend(title='Страна', fontsize=10, title_fontsize=12, loc='upper right')

        # Добавляем сетку
        plt.grid(True, which='both', linestyle='--', linewidth=0.7, color='gray', alpha=0.7)

        # Подгонка макета
        plt.tight_layout()

        # Отображаем линейный график в Streamlit
        st.pyplot(plt)

    # Столбчатая диаграмма
    with tab2:
        st.write("Столбчатая диаграмма для сравнения {} по странам.".format(metrics_mapping[selected_metric]))
        plt.figure(figsize=(12, 6))
        sns.barplot(data=filtered_data, x='year', y=selected_metric, hue='Страна', ci=None)
        
        # Настройка осей
        plt.title('Сравнение {} по странам'.format(metrics_mapping[selected_metric]), fontsize=16, weight='bold', color='darkblue')
        plt.xlabel('Год', fontsize=12, color='darkgreen')
        plt.ylabel(metrics_mapping[selected_metric], fontsize=12, color='darkgreen')
        plt.xticks(rotation=45, fontsize=10)
        plt.yticks(fontsize=10)
        plt.legend(title='Страна', fontsize=10, title_fontsize=12, loc='upper right')

        # Отображаем столбчатую диаграмму в Streamlit
        st.pyplot(plt)

    # Интерактивные пояснения
    with st.expander("Интерактивные пояснения"):
        st.write("""На графиках вы можете увидеть изменения выбранного показателя по странам и годам. 
            Столбчатая диаграмма позволяет сравнить показатели между странами за выбранные годы.
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
                pickable=True,
            ),
        ],
        tooltip={
            "text": "{Страна}\n{Лат}, {Лон}"
        },
    ))
else:
    st.error("Не удалось получить данные для выбранных стран.")
