import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Загрузка данных
file_path = "aggregated_results.xlsx"  # Укажите путь к вашему файлу
df_pandas = pd.read_excel(file_path)

# Проверка загруженных данных
st.write("Исходные данные:")
st.write(df_pandas.head())  # Отображаем первые 5 строк

# Преобразуем данные
df_pandas['year'] = df_pandas['country'].str[-4:]  # Извлечение года
df_pandas['country'] = df_pandas['country'].str[:-5]  # Извлечение названия страны

# Проверка преобразованных данных
st.write("Преобразованные данные:")
st.write(df_pandas.head())

# Настройка стиля графика
plt.style.use('ggplot')

# Визуализация для всех стран
plt.figure(figsize=(12, 6))

# Построение графика
sns.lineplot(data=df_pandas, x='year', y='Модерированная тяжесть для всех', hue='country', dashes=False)

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
