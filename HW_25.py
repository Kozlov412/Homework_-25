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
