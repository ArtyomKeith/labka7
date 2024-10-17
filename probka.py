import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Загрузка данных
file_path = "aggregated_results.xlsx"  # Замените на ваш путь к файлу
df_pandas = pd.read_excel(file_path)

# Проверка данных
st.write(df_pandas.head())

# Объединение данных по годам для всех стран
def combine_data_all_countries(df):
    df_combined = df.groupby(['year', 'country']).mean(numeric_only=True).reset_index()
    return df_combined

# Объединение данных
df_combined = combine_data_all_countries(df_pandas)

# Визуализация для всех стран
plt.figure(figsize=(12, 6))

# Используем sns.lineplot для отображения всех стран
sns.lineplot(data=df_combined, x='year', y='F_mod_sev_tot', hue='country')

# Добавляем заголовок
plt.title('Изменение продовольственной безопасности (модерированная тяжесть) по годам для всех стран')

# Подписи к осям
plt.xlabel('Год')
plt.ylabel('Модерированная тяжесть продовольственной безопасности')

# Поворачиваем метки на оси X
plt.xticks(rotation=45, fontsize=10)

plt.tight_layout()  # Автоматическая подгонка графика

# Отображение графика в Streamlit
st.pyplot(plt)
