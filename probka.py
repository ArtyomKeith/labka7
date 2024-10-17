import streamlit as st
import pandas as pd
import dask.dataframe as dd
import matplotlib.pyplot as plt
import seaborn as sns

# Заголовок дашборда
st.title("Анализ продовольственной безопасности по странам")

# Загрузка данных
file_path = "aggregated_results.xlsx"  # Используйте ваш путь к файлу
df_pandas = pd.read_excel(file_path)

# Выбор страны для анализа
country = st.selectbox("Выберите страну для анализа", df_pandas['country'].unique())

# Фильтрация данных по выбранной стране
country_data = df_pandas[df_pandas['country'] == country]

# Визуализация трендов
st.subheader(f'Тренды для {country}')

# Используем средние значения по годам
df_combined = country_data.groupby('year').mean(numeric_only=True)

# Создаем график с помощью matplotlib
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=df_combined, x='year', y='F_mod_sev_tot', ax=ax)  # Замените на правильное имя столбца
ax.set_title(f'Изменение продовольственной безопасности (модерированная тяжесть) в {country}')
ax.set_xlabel('Год')
ax.set_ylabel('Модерированная тяжесть продовольственной безопасности')
plt.xticks(rotation=45)

# Отображение графика в Streamlit
st.pyplot(fig)

# Вывод средних значений в виде таблицы
st.subheader("Средние значения показателей")
st.dataframe(df_combined)
