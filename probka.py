import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Загрузка данных
file_path = "aggregated_results.xlsx"  # Замените на ваш путь к файлу
df_pandas = pd.read_excel(file_path)

# Переименовываем колонки на русский язык
df_pandas.rename(columns={
    'F_mod_sev_ad': 'Модерированная тяжесть для взрослых',
    'F_sev_ad': 'Серьезная тяжесть для взрослых',
    'F_mod_sev_child': 'Модерированная тяжесть для детей',
    'F_sev_child': 'Серьезная тяжесть для детей',
    'F_mod_sev_tot': 'Модерированная тяжесть для всех',
    'F_sev_tot': 'Серьезная тяжесть для всех',
}, inplace=True)

# Проверка данных с новыми названиями колонок
st.write(df_pandas.head())

# Функция для объединения данных по годам и странам
def combine_data_all_countries(df):
    df_combined = df.groupby(['year', 'country']).mean(numeric_only=True).reset_index()
    return df_combined

# Объединение данных
df_combined = combine_data_all_countries(df_pandas)

# Пивотируем данные для построения графика
df_pivot = df_combined.pivot(index='year', columns='country', values='Модерированная тяжесть для всех')

# Настройка стиля графика
plt.style.use('ggplot')

# Визуализация для всех стран
plt.figure(figsize=(12, 6))

# Построение графика
sns.lineplot(data=df_pivot, dashes=False)

# Убираем ненужные метки и выставляем года
plt.xticks(df_pivot.index, rotation=45, fontsize=10)

# Добавляем заголовок и подписи
plt.title('Изменение продовольственной безопасности по годам для всех стран', fontsize=16)
plt.xlabel('Год', fontsize=12)
plt.ylabel('Модерированная тяжесть продовольственной безопасности', fontsize=12)

# Настройка для улучшения отображения легенды и подписей
plt.legend(title='Страны', fontsize=10, title_fontsize=12)
plt.tight_layout()  # Автоматическая подгонка графика

# Отображение графика в Streamlit
st.pyplot(plt)
