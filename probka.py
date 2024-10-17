import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Создание тестовых данных
data = {
    'year': ['2014', '2014', '2015', '2015', '2016', '2016', '2017', '2017'],
    'country': ['Казахстан', 'Кыргызстан', 'Казахстан', 'Кыргызстан', 'Казахстан', 'Кыргызстан', 'Казахстан', 'Кыргызстан'],
    'Модерированная тяжесть для всех': [0.1, 0.2, 0.15, 0.25, 0.2, 0.3, 0.25, 0.35]
}

df_pandas = pd.DataFrame(data)

# Проверка загруженных данных
st.write("Тестовые данные:")
st.write(df_pandas)

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
