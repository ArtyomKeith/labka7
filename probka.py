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
    'TAIJ': 'Таджикистан',  # исправлено сокращение
    'UZB': 'Узбекистан'     # исправлено сокращение
}

# Заменяем названия стран в столбце 'country'
df_pandas['country'] = df_pandas['country'].replace(country_mapping)

# Выбор стран для отображения
countries = df_pandas['country'].unique().tolist()
selected_countries = st.multiselect("Выберите страны для отображения:", countries, default=countries)

# Фильтруем данные по выбранным странам
filtered_data = df_pandas[df_pandas['country'].isin(selected_countries)]

# Проверка, что данные не пустые после фильтрации
if not filtered_data.empty:
    # Настройка графика
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=filtered_data, x='year', y='F_mod_sev_tot', hue='country', marker='o')

    # Настройка осей
    plt.xticks(filtered_data['year'].unique(), rotation=45)
    plt.title('Изменение продовольственной безопасности по годам для выбранных стран')
    plt.xlabel('Год')
    plt.ylabel('Модерированная тяжесть продовольственной безопасности')

    # Отображаем график в Streamlit
    st.pyplot(plt)
else:
    st.error("Не удалось получить данные для выбранных стран.")
