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

# Выбор стран для отображения
countries = df_pandas['Страна'].unique().tolist()
selected_countries = st.multiselect("Выберите страны для отображения:", countries, default=countries)

# Фильтруем данные по выбранным странам
filtered_data = df_pandas[df_pandas['Страна'].isin(selected_countries)]

# Проверка, что данные не пустые после фильтрации
if not filtered_data.empty:
    # Настройка стиля
    plt.style.use('ggplot')  # Используем стиль ggplot, который встроен в Matplotlib

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
else:
    st.error("Не удалось получить данные для выбранных стран.")
