import streamlit as st
import pandas as pd

# Путь к вашему файлу
file_path = "aggregated_results.xlsx"  # Укажите путь к вашему файлу

# Используем pandas для загрузки данных
df_pandas = pd.read_excel(file_path)

# Проверка загруженных данных
st.write("Загруженные данные:")
st.write(df_pandas)

# Проверка названий столбцов
st.write("Названия столбцов:")
st.write(df_pandas.columns.tolist())  # Вывод названий столбцов в виде списка

# Проверка наличия уникальных значений в столбце 'country'
if 'country' in df_pandas.columns:
    st.write("Уникальные значения в колонке country:")
    st.write(df_pandas['country'].unique())
else:
    st.write("Столбца 'country' нет в данных.")

# Проверка наличия столбца 'year'
if 'year' in df_pandas.columns:
    st.write("Уникальные значения в колонке year:")
    st.write(df_pandas['year'].unique())
else:
    st.write("Столбца 'year' нет в данных.")
