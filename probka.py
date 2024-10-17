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
st.write(df_pandas.columns.tolist())

# Настройка стиля графика
plt.style.use('ggplot')

# Создание столбца с годами из названия страны
df_pandas['year'] = df_pandas['country'].str[-4:]  # Извлекаем последние 4 символа для года
df_pandas['country'] = df_pandas['country'].str[:-5]  # Убираем год из названия страны

# Проверка наличия необходимых данных для построения графика
if 'F_mod_sev_tot' in df_pandas.columns and 'country' in df_pandas.columns and 'year' in df_pandas.columns:
    # Поворот датафрейма для удобства визуализации
    df_pivot = df_pandas.pivot(index='year', columns='country', values='F_mod_sev_tot')

    # Визуализация для всех стран
    plt.figure(figsize=(12, 6))

    # Построение графика
    sns.lineplot(data=df_pivot)

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
    st.error("Отсутствуют необходимые столбцы для построения графика.")
