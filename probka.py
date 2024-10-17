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

# Заголовок приложения
st.title("Анализ продовольственной безопасности стран Центральной Азии")
st.markdown("""
Это приложение визуализирует динамику продовольственной безопасности в Казахстане, Кыргызстане, Таджикистане и Узбекистане за разные годы.
Вы можете выбрать страны и диапазон годов для отображения на графике.
""")

# Выбор стран для отображения
countries = df_pandas['Страна'].unique().tolist()
selected_countries = st.multiselect("Выберите страны для отображения:", countries, default=countries)

# Выбор диапазона годов
min_year = int(df_pandas['year'].min())
max_year = int(df_pandas['year'].max())
selected_years = st.slider("Выберите диапазон годов:", min_year, max_year, (min_year, max_year))

# Фильтруем данные по выбранным странам и годам
filtered_data = df_pandas[(df_pandas['Страна'].isin(selected_countries)) & 
                          (df_pandas['year'].between(*selected_years))]

# Вычисление средней продовольственной безопасности для выбранных стран
if not filtered_data.empty:
    avg_security = filtered_data.groupby('Страна')['F_mod_sev_tot'].mean()
    st.subheader("Средняя продовольственная безопасность для выбранных стран:")
    st.write(avg_security)

    # Настройка стиля графика
    plt.figure(figsize=(12, 6))
    sns.set_palette("Set2")  # Красочная палитра для линий
    sns.lineplot(data=filtered_data, x='year', y='F_mod_sev_tot', hue='Страна', marker='o', linewidth=2.5)

    # Оформление графика
    plt.title('Динамика продовольственной безопасности', fontsize=18, weight='bold', color='navy')
    plt.xlabel('Год', fontsize=12, color='darkgreen')
    plt.ylabel('Модерированная тяжесть продовольственной безопасности', fontsize=12, color='darkgreen')
    plt.grid(True, linestyle='--', linewidth=0.6, alpha=0.7)
    
    # Отображение графика
    st.pyplot(plt)
else:
    st.error("Не удалось получить данные для выбранных стран.")
