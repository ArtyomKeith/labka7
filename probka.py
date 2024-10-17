import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Загрузка данных
file_path = "aggregated_results.xlsx"  # Замените на ваш путь к файлу
df_pandas = pd.read_excel(file_path)

# Проверка загруженных данных
st.write("Исходные данные:")
st.write(df_pandas.head())

# Преобразуем данные в длинный формат
df_pandas['year'] = df_pandas['country'].str[-4:]  # Извлечение года
df_pandas['country'] = df_pandas['country'].str[:-5]  # Извлечение названия страны (удаление последних 5 символов)
df_pandas = df_pandas.rename(columns={
    'F_mod_sev_ad': 'Модерированная тяжесть для взрослых',
    'F_sev_ad': 'Серьезная тяжесть для взрослых',
    'F_mod_sev_child': 'Модерированная тяжесть для детей',
    'F_sev_child': 'Серьезная тяжесть для детей',
    'F_mod_sev_tot': 'Модерированная тяжесть для всех',
    'F_sev_tot': 'Серьезная тяжесть для всех',
})

# Проверка преобразованных данных
st.write("Преобразованные данные:")
st.write(df_pandas.head())

# Функция для объединения данных по годам и странам
def combine_data_all_countries(df):
    df_combined = df.groupby(['year', 'country']).mean(numeric_only=True).reset_index()
    return df_combined

# Объединение данных
df_combined = combine_data_all_countries(df_pandas)

# Проверка объединенных данных
st.write("Объединенные данные:")
st.write(df_combined)

# Настройка стиля графика
plt.style.use('ggplot')

# Визуализация для всех стран
plt.figure(figsize=(12, 6))

# Построение графика
sns.lineplot(data=df_combined, x='year', y='Модерированная тяжесть для всех', hue='country', dashes=False)

# Убираем ненужные метки и выставляем года
plt.xticks(rotation=45, fontsize=10)

# Добавляем заголовок и подписи
plt.title('Изменение продовольственной безопасности по годам для всех стран', fontsize=16)
plt.xlabel('Год', fontsize=12)
plt.ylabel('Модерированная тяжесть продовольственной безопасности', fontsize=12)

# Настройка для улучшения отображения легенды и подписей
plt.legend(title='Страны', fontsize=10, title_fontsize=12)
plt.tight_layout()  # Автоматическая подгонка графика

# Отображение графика в Streamlit
st.pyplot(plt)
