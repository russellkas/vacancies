def filter_vacancies(vacancies_list: list, filter_words: list) -> list:
    """
    Функция фильтрует список вакансий на основе списка ключевых слов.

    Аргументы:
    - vacancies_list (list): Список объектов вакансий.
    - filter_words (list): Список ключевых слов для фильтрации.

    Возвращает:
    - filtered_vacancies (list): Отфильтрованный список вакансий.
    """
    filtered_vacancies = []
    for vacancy in vacancies_list:
        description_lower = vacancy.description.lower()
        for keyword in filter_words:
            if keyword.lower() in description_lower:
                filtered_vacancies.append(vacancy)
    return filtered_vacancies


def get_vacancies_by_salary(vacancies: list, salary_range: tuple) -> list:
    """
    Функция возвращает список вакансий с учетом заданного диапазона зарплат.

    Аргументы:
    - vacancies (list): Список объектов вакансий.
    - salary_range (str): Диапазон зарплат в формате "min-max".

    Возвращает:
    - Список вакансий с зарплатой в указанном диапазоне.
    """
    min_salary, max_salary = salary_range[0], salary_range[1]
    return [vacancy for vacancy in vacancies if min_salary <= int(vacancy.salary) <= max_salary]


def sort_vacancies(vacancies_list: list) -> list:
    """
    Функция сортирует список вакансий по убыванию зарплаты.

    Аргументы:
    - vacancies_list (list): Список объектов вакансий.

    Возвращает:
    - Отсортированный список вакансий по убыванию зарплаты.
    """
    sorted_vacancies = sorted(vacancies_list, key=lambda x: x.salary, reverse=True)
    return sorted_vacancies


def get_top_vacancies(vacancies_list: list, top_n: int) -> list:
    """
    Функция возвращает указанное количество самых высокооплачиваемых вакансий.

    Аргументы:
    - vacancies_list (list): Список объектов вакансий.
    - top_n (int): Количество вакансий для возврата.

    Возвращает:
    - Список top_n самых высокооплачиваемых вакансий.
    """
    if vacancies_list:
        return vacancies_list[:top_n]
    else:
        return ["Вакансий не найдено"]


def print_vacancies(vacancies_list: list) -> None:
    """
    Функция выводит информацию о вакансиях.

    Аргументы:
    - vacancies_list (list): Список объектов вакансий.

    Возвращает:
    - None. Просто выводит информацию о вакансиях.
    """
    for vacancy in vacancies_list:
        print(f'{vacancy}\n')



def parse_top_n(raw: str) -> int | None:
    try:
        value = int(raw)
        if value > 0:
            return value
        else:
            print("Enter number > 0")
            return None
    except ValueError:
        print("Enter correct number (e.g. 10)")
        return None
    

def parse_salary_range(raw: str) -> tuple[int, int] | None:
    try:
        parts = raw.split("-")

        if len(parts) != 2:
            print("The format has to be min-max (e.g. 2000-4000)")
            return None
        
        min_salary, max_salary = map(int, parts)

        if min_salary < 0 or max_salary < 0:
            print("The salary can't be less than 0")
            return None
        
        if min_salary > max_salary:
            print("The min salry can't be more than the max salary")
            return None
        
        return min_salary, max_salary
    except ValueError:
        print("The format has to be min-max (e.g. 2000-4000)")
        return None
    

def input_top_n():
    while True:
        raw = input("Enter number of vacancies (top N): ")
        result = parse_top_n(raw)
        if result is not None:
            return result
        

def input_salary_range():
    while True:
        raw = input("Enter salary range: ")
        result = parse_salary_range(raw)
        if result is not None:
            return result
        