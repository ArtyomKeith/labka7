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

# Получаем список стран из названий столбцов
countries = [col.split('_')[0] for col in df_pandas.columns if '_' in col]
unique_countries = list(set(countries))

# Выбор стран для отображения
selected_countries = st.multiselect("Выберите страны для отображения:", unique_countries, default=unique_countries)

# Фильтрация данных по выбранным странам
filtered_columns = [col for col in df_pandas.columns if col.split('_')[0] in selected_countries]
filtered_df = df_pandas[['year'] + filtered_columns]

# Проверка наличия необходимых данных для построения графика
if filtered_df.shape[1] > 1:
    # Настройка графика
    plt.figure(figsize=(12, 6))
    filtered_df.set_index('year').T.plot()

    # Убираем ненужные метки и выставляем года
    plt.xticks(rotation=45, fontsize=10)

    # Добавляем заголовок и подписи
    plt.title('Изменение продовольственной безопасности по годам для выбранных стран', fontsize=16)
    plt.xlabel('Год', fontsize=12)
    plt.ylabel('Модерированная тяжесть продовольственной безопасности', fontsize=12)

    # Настройка для улучшения отображения легенды и подписей
    plt.legend(title='Страны', fontsize=10, title_fontsize=12)
    plt.tight_layout()  # Автоматическая подгонка графика

    # Отображение графика в Streamlit
    st.pyplot(plt)
else:
    st.error("Отсутствуют необходимые столбцы для построения графика.")
