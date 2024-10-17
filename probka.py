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
countries = list(set(col.split('_')[0] for col in df_pandas.columns if '_' in col))

# Выбор стран для отображения
selected_countries = st.multiselect("Выберите страны для отображения:", countries, default=countries)

# Создаем новый DataFrame для выбранных стран
filtered_data = []

for country in selected_countries:
    country_data = df_pandas[['year', f'{country}_2014', f'{country}_2015', f'{country}_2016', f'{country}_2017']]
    country_data = country_data.melt(id_vars=['year'], var_name='country', value_name='F_mod_sev_tot')
    filtered_data.append(country_data)

# Объединяем данные всех выбранных стран
if filtered_data:
    final_df = pd.concat(filtered_data)

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
    st.error("Выберите хотя бы одну страну для отображения.")
