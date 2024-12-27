from marvel import full_dict
from pprint import pprint
from typing import Dict, Any, List, Tuple, Optional


def get_sortable_year(year_value: Optional[Any]) -> int:
    try:
        return int(year_value)
    except (ValueError, TypeError):
        return float("inf")  # Бесконечность для некорректных значений


def get_sortable_title(item: Tuple[int, Dict[str, Any]]) -> str:
    title = item[1].get("title")
    return title if isinstance(title, str) else ""


# 1. Ввод и преобразование ID с проверкой (с использованием map)
filtered_ids: List[int] = []
while not filtered_ids:
    user_input = input("Введите id фильмов через пробел: ")
    input_ids = user_input.split()

    def convert_to_int_or_none(id_str: str) -> Optional[int]:
        try:
            return int(id_str)
        except ValueError:
            return None

    converted_ids = list(map(convert_to_int_or_none, input_ids)) # Применение map

    for id_ in converted_ids:
        if id_ is not None and id_ in full_dict:
            filtered_ids.append(id_)
        elif id_ is not None: # Проверка на None, чтобы избежать KeyError
            print(f"Фильма с ID {id_} не существует.")
        else:
            print(f"Некорректный ID . Он будет проигнорирован.") # Исправлено сообщение об ошибке

    if not filtered_ids:
        print("Не введено ни одного корректного ID. Попробуйте еще раз.")


# 2. Фильтрация по ID
filtered_dict: Dict[int, Any] = {
    k: v for k, v in full_dict.items() if k in filtered_ids
}

# 3. Уникальные режиссеры (с обработкой отсутствующего ключа)
unique_directors: set = {
    movie.get("director") for movie in full_dict.values() if movie.get("director")
}

# 4. Годы как строки (с обработкой отсутствующего ключа)
string_year_dict = {
    k: dict(v, year=str(v["year"]) if "year" in v else None)
    for k, v in full_dict.items()
}

# 5. Фильмы на "Ч" (с проверкой на тип)
films_starting_with_ch: Dict[int, Any] = {
    k: v
    for k, v in full_dict.items()
    if isinstance(v.get("title"), str) and v.get("title").startswith("Ч")
}

# 6. Сортировка по году (с преобразованием в словарь)
sorted_by_year: Dict[int, Any] = dict(
    sorted(full_dict.items(), key=lambda item: get_sortable_year(item[1].get("year")))
)    


# 7. Сортировка по году и названию (с преобразованием в словарь)
sorted_by_year_and_title: Dict[int, Any] = dict(
    sorted(
        full_dict.items(), # Используем весь full_dict
        key=lambda item: (get_sortable_year(item[1].get("year")), get_sortable_title(item)), # Сортировка по году, затем по названию
    )
)

# 8. Фильтрация и сортировка в одной строке (с filter и sorted)
filtered_and_sorted_oneline: Dict[int, Any] = dict(sorted(filter(lambda item: get_sortable_year(item[1].get("year")) > 2020, full_dict.items()), key=lambda item: (get_sortable_year(item[1].get("year")), get_sortable_title(item))))

# 9. Функция process_marvel_data для обработки данных Marvel
def process_marvel_data(data: Dict[int, Dict[str, Any]]) -> List[Tuple[int, str]]:
    """
    Обрабатывает данные Marvel: возвращает список кортежей (id, title) фильмов,
    отсортированных по названию в алфавитном порядке.
    """
    result: List[Tuple[int, str]] = []
    for id_, movie_data in data.items():
        title = movie_data.get("title")
        if isinstance(title, str):  # Проверка, что title - строка
            result.append((id_, title))
    return sorted(result, key=lambda item: item[1])  # Сортировка по названию


# Вывод результатов с использованием pprint
print("\nЗадание 2: Фильтрация фильмов по введенным ID.")
pprint(filtered_dict)

print("\nЗадание 3: Получение уникальных режиссеров.")
pprint(unique_directors)

print("\nЗадание 4: Копирование словаря с годами в строковом формате.")
pprint(string_year_dict)

print("\nЗадание 5: Фильмы, начинающиеся на букву 'Ч'.")
pprint(films_starting_with_ch)

print("\nЗадание 6: Сортировка фильмов по году.")
pprint(sorted_by_year)

print("\nЗадание 7: Сортировка фильмов по году и названию.")
pprint(sorted_by_year_and_title)

print("\nЗадание 8: Фильтрация и сортировка фильмов после 2020 года в одной строке.")
pprint(filtered_and_sorted_oneline)

# Вызов process_marvel_data и вывод результата
processed_data = process_marvel_data(filtered_dict)  # Обрабатываем filtered_dict
print("\nЗадание 9: Обработка данных Marvel (id, title, сортировка по title).")
pprint(processed_data)


# Проверка mypy выявила ошибки:
# HW#25.py:8: error:Argument 1 to "int" has incompatible type "Any | None"; expected "str | Buffer | SupportsInt | SupportsIndex | SupportsTrunc"  [arg-type]
#HW#25.py:10: error: Incompatible return value type (got "float", expected "int")  [return-value]
#HW#25.py:64: error: Item "None" of "Any | None" has no attribute "startswith"  [union-attr]
#Found 3 errors in 1 file (checked 1 source file)