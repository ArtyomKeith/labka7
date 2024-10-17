import streamlit as st
import pandas as pd

# Загрузка данных
file_path = "aggregated_results.xlsx"  # Укажите путь к вашему файлу
df_pandas = pd.read_excel(file_path)

# Вывод информации о DataFrame
st.write("Проверка загруженных данных:")
st.write(df_pandas.head())
st.write(df_pandas.info())

# Проверка уникальных значений в колонках
st.write("Уникальные значения в колонке country:")
st.write(df_pandas['country'].unique())

st.write("Уникальные значения в колонке F_mod_sev_tot:")
st.write(df_pandas['F_mod_sev_tot'].unique())

# Очистка данных
df_pandas['country'] = df_pandas['country'].str.strip()
df_pandas['year'] = df_pandas['year'].str.strip()
