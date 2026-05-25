import pandas as pd
import re

# === Шаг 0: Загрузка и подготовка данных ===
df = pd.read_xml('news_mega_bulk_2026-05-25_17-06-33.xml')
print(df.columns.tolist())
df=df.rename(columns={'pubDate':'pub_date'})
# Приводим даты к формату datetime, а пропуски в тексте заполняем пустой строкой
df['pub_date'] = pd.to_datetime(df['pub_date'], errors='coerce',utc=True)
text_data = df['description'].fillna('').astype(str)


# === 1. Количество уникальных слов ===
# Объединяем весь текст, приводим к нижнему регистру и выделяем слова регулярным выражением
all_text = " ".join(text_data).lower()
all_words = re.findall(r'\b\w+\b', all_text)
unique_words_count = len(set(all_words))


# === 2. Метрики количества слов в записях ===
# Считаем количество слов в каждой отдельной статье
word_counts = text_data.apply(lambda x: len(re.findall(r'\b\w+\b', x)))

word_stats = {
    "min": word_counts.min(),
    "max": word_counts.max(),
    "mean": word_counts.mean(),
    "median": word_counts.median()
}


# === 3. Диапазон дат опубликования ===
min_date = df['pub_date'].min()
max_date = df['pub_date'].max()


# === 4. Доля пропусков по каждому атрибуту ===
# .isnull().mean() возвращает долю (от 0.0 до 1.0) missing значений для каждой колонки
missing_share = df.isnull().mean()


# === ВЫВОД ИНФОРМАЦИИ ===
print(f"1. Количество уникальных слов в датасете: {unique_words_count:,}\n")

print("2. Статистика количества слов в записях:")
print(f" - Минимальное: {word_stats['min']}")
print(f" - Максимальное: {word_stats['max']}")
print(f" - Среднее: {word_stats['mean']:.2f}")
print(f" - Медианное: {word_stats['median']:.1f}\n")

print(f"3. Диапазон дат публикации:")
print(f" - С: {min_date}")
print(f" - По: {max_date}\n")

print("4. Доля пропусков в записях по атрибутам:")
for col, share in missing_share.items():
    print(f" - {col}: {share:.2%} (пропущено)")

