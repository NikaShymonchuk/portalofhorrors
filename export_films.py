import sqlite3
import json
from datetime import datetime
print("🎬 Починаємо експорт всіх фільмів з бази даних...")
try:
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    print("✅ Підключено до mydatabase.db")
except Exception as e:
    print(f"❌ Помилка підключення до бази: {e}")
    exit(1)
try:
    cursor.execute("SELECT * FROM film")
    films_raw = cursor.fetchall()
    print(f"📊 Знайдено фільмів у базі: {len(films_raw)}")
except Exception as e:
    print(f"❌ Помилка читання таблиці film: {e}")
    conn.close()
    exit(1)
columns = [description[0] for description in cursor.description]
print(f"📋 Колонки: {', '.join(columns)}")
films_data = []
for i, film in enumerate(films_raw, start=1):
    film_dict = {'id': i}
    for col_index, column in enumerate(columns):
        value = film[col_index]
        if column == 'year' and value:
            try:
                if isinstance(value, str):
                    if '-' in value:
                        year = value.split('-')[0]
                    else:
                        year = value
                else:
                    year = str(value)
                film_dict[column] = year
            except:
                film_dict[column] = str(value) if value else ''
        elif value is None:
            film_dict[column] = ''
        else:
            film_dict[column] = value
    films_data.append(film_dict)
    print(f"  ✓ Експортовано: {film_dict.get('name', 'Unknown')}")

conn.close()
try:
    with open('films.json', 'w', encoding='utf-8') as f:
        json.dump(films_data, f, ensure_ascii=False, indent=2)
    print(f"\n✅ Успішно експортовано {len(films_data)} фільмів у films.json")
except Exception as e:
    print(f"❌ Помилка збереження файлу: {e}")
    exit(1)
print(f"\n📄 Приклад першого фільму:")
print(json.dumps(films_data[0], ensure_ascii=False, indent=2))
print(f"\n📊 Статистика:")
print(f"  - Всього фільмів: {len(films_data)}")
countries = set(film.get('country', '') for film in films_data if film.get('country'))
print(f"  - Країн: {len(countries)} ({', '.join(sorted(countries))})")
genres = set()
for film in films_data:
    genre = film.get('genre', '')
    if genre:
        genres.update([g.strip() for g in genre.split(',')])
print(f"  - Унікальних жанрів: {len(genres)}")
years = set(film.get('year', '') for film in films_data if film.get('year'))
print(f"  - Роки: від {min(years) if years else 'N/A'} до {max(years) if years else 'N/A'}")
print(f"\n🎯 Готово! Тепер скопіюй films.json у docs/data/")
print(f"   Команда: cp films.json docs/data/")