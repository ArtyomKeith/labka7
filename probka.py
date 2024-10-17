import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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

# Проверка наличия столбца 'Модерированная тяжесть для всех'
if 'Модерированная тяжесть для всех' in df_pandas.columns:
    st.write("Проверка на пропуски в столбце 'Модерированная тяжесть для всех':")
    st.write(df_pandas['Модерированная тяжесть для всех'].isnull().sum())
else:
    st.write("Столбца 'Модерированная тяжесть для всех' нет в данных.")

# Приводим year к строковому типу, если это необходимо
if 'year' in df_pandas.columns:
    df_pandas['year'] = df_pandas['year'].astype(str)
else:
    st.write("Столбца 'year' нет в данных.")

# Настройка стиля графика
plt.style.use('ggplot')

# Визуализация для всех стран
plt.figure(figsize=(12, 6))

# Построение графика
if 'Модерированная тяжесть для всех' in df_pandas.columns and 'year' in df_pandas.columns:
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
else:
    st.write("Не удалось построить график, так как отсутствуют необходимые столбцы.")
