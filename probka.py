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

# Визуализация для всех стран
plt.figure(figsize=(12, 6))

# Проверка наличия необходимых данных для построения графика
if 'F_mod_sev_tot' in df_pandas.columns and 'country' in df_pandas.columns and 'year' in df_pandas.columns:
    # Построение графика
    sns.lineplot(data=df_pandas, x='year', y='F_mod_sev_tot', hue='country', dashes=False)

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
