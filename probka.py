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

# Маппинг стран
country_mapping = {
    'KGZ': 'Киргизстан',
    'UZB': 'Узбекистан',
    'KAZ': 'Казахстан',
    'TJK': 'Таджикистан'
}

# Выбор стран для отображения
selected_countries = st.multiselect("Выберите страны для отображения:", list(country_mapping.keys()), default=list(country_mapping.keys()))

# Проверяем, выбраны ли страны
if not selected_countries:
    st.warning("Пожалуйста, выберите хотя бы одну страну.")
else:
    # Создаем новый DataFrame для выбранных стран
    filtered_data = []

    for country in selected_countries:
        # Фильтруем данные по стране и годам
        country_data = df_pandas[df_pandas['country'] == country].copy()  # Предполагаем, что 'country' - это название страны

        # Проверяем, есть ли данные для этой страны
        if not country_data.empty:
            # Добавляем страну и соответствующие значения для годовых данных
            melted_data = country_data[['year', 'F_mod_sev_tot']].copy()
            melted_data['country'] = country_mapping[country]
            filtered_data.append(melted_data)
        else:
            st.warning(f"Нет данных для {country}")

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
