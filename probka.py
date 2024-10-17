import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Путь к вашему файлу
file_path = "aggregated_results.xlsx"  # Укажите путь к вашему файлу

# Используем pandas для загрузки данных
df_pandas = pd.read_excel(file_path)

# Проверка загруженных данных
st.write("Загруженные данные:")
st.write(df_pandas)

# Проверка названий столбцов
st.write("Названия столбцов:")
st.write(df_pandas.columns.tolist())

# Настройка стиля графика
plt.style.use('ggplot')

# Получаем список стран из названий столбцов
country_mapping = {
    'KGZ': 'Киргизстан',
    'UZB': 'Узбекистан',
    'KAZ': 'Казахстан',
    'TJK': 'Таджикистан'
}

countries = sorted(country_mapping.keys())

# Выбор стран для отображения
selected_countries = st.multiselect("Выберите страны для отображения:", countries, default=countries)

# Проверяем, выбраны ли страны
if not selected_countries:
    st.warning("Пожалуйста, выберите хотя бы одну страну.")
else:
    # Создаем новый DataFrame для выбранных стран
    filtered_data = []

    for country in selected_countries:
        # Фильтрация столбцов по стране
        country_columns = df_pandas.filter(like=country).columns.tolist()

        # Проверяем наличие данных
        st.write(f"Выбраны столбцы для {country}: {country_columns}")
        
        # Проверяем, есть ли у нас данные для этой страны
        if country_columns and 'year' in df_pandas.columns:
            country_data = df_pandas[['year'] + country_columns]

            # Проверяем, достаточно ли столбцов для выполнения melt
            if len(country_data.columns) > 1:
                try:
                    # Переименовываем столбцы, чтобы избежать конфликта с value_name
                    renamed_columns = {col: col.replace('_', ' ') for col in country_columns}
                    country_data.rename(columns=renamed_columns, inplace=True)

                    # Проводим melt
                    melted_data = country_data.melt(id_vars=['year'], var_name='country', value_name='F_mod_sev_tot')

                    # Заменяем коды стран на названия
                    melted_data['country'] = melted_data['country'].apply(lambda x: country_mapping.get(x.split(' ')[0], x))
                    filtered_data.append(melted_data)
                except Exception as e:
                    st.error(f"Ошибка при обработке данных для страны {country}: {e}")

    # Объединяем данные всех выбранных стран
    if filtered_data:
        final_df = pd.concat(filtered_data, ignore_index=True)

        # Построение графика
        plt.figure(figsize=(12, 6))
        sns.lineplot(data=final_df, x='year', y='F_mod_sev_tot', hue='country', dashes=False)

        # Убираем ненужные метки и выставляем года
        plt.xticks(rotation=45, fontsize=10)

        # Добавляем заголовок и подписи
        plt.title('Изменение продовольственной безопасности по годам для выбранных стран', fontsize=16)
        plt.xlabel('Год', fontsize=12)
        plt.ylabel('Модерированная тяжесть продовольственной безопасности', fontsize=12)

        # Настройка для улучшения отображения легенды и подписей
        plt.legend(title='Страны', fontsize=10, title_fontsize=12)
        plt.tight_layout()  # Автоматическая подгонка графика

        # Отображение графика в Streamlit
        st.pyplot(plt)
    else:
        st.error("Не удалось получить данные для выбранных стран.")
