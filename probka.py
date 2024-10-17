import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Путь к файлу
file_path = "aggregated_results.xlsx"
df_pandas = pd.read_excel(file_path)

# Преобразование названий стран
df_pandas['Страна'] = df_pandas['country'].replace({
    'Kazakhstan': 'Казахстан',
    'Kyrgyzstan': 'Кыргызстан',
    'Tajikistan': 'Таджикистан',
    'Uzbekistan': 'Узбекистан'
})

# Заголовок и описание
st.title('Динамика продовольственной безопасности в Центральной Азии')
st.write('На этом графике представлена информация о продовольственной безопасности для стран Центральной Азии за различные годы.')

# Добавление фильтра по годам
years = df_pandas['year'].unique()
selected_years = st.slider('Выберите диапазон годов:', min_value=int(min(years)), max_value=int(max(years)), value=(int(min(years)), int(max(years))))

# Фильтрация данных по выбранным годам
filtered_data = df_pandas[df_pandas['year'].between(selected_years[0], selected_years[1])]

# Выбор стран
countries = df_pandas['Страна'].unique()
selected_countries = st.multiselect('Выберите страны для отображения:', countries, default=countries)

# Фильтрация по выбранным странам
filtered_data = filtered_data[filtered_data['Страна'].isin(selected_countries)]

# Построение графика
plt.figure(figsize=(10, 6))
sns.set(style="whitegrid")

# Проверяем, что данные существуют
if not filtered_data.empty:
    sns.lineplot(data=filtered_data, x='year', y='F_mod_sev_tot', hue='Страна', marker="o")

    plt.title('Изменение продовольственной безопасности по странам', fontsize=16)
    plt.xlabel('Год', fontsize=12)
    plt.ylabel('Модерированная тяжесть', fontsize=12)
    plt.xticks(rotation=45)
    plt.legend(title='Страны')

    st.pyplot(plt)
else:
    st.warning("Нет данных для выбранных стран или диапазона годов.")

# Добавление статистики
st.subheader('Средний уровень продовольственной безопасности по странам:')
average_values = filtered_data.groupby('Страна')['F_mod_sev_tot'].mean()
st.write(average_values)
