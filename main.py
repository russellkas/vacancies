from src.job import HeadHunterAPI
from src.vacancy import Vacancy
from src.utils import *
from src.json import JSONSaver


def user_interaction():
    search_query = input("Введите поисковый запрос: ").lower()
    top_n = input_top_n()
    filter_words = input("Введите ключевые слова для фильтрации вакансий: ").split()
    salary_range = input_salary_range()

    hh_api = HeadHunterAPI()
    hh_vacancies = hh_api.get_vacancies(search_query)

    if hh_vacancies:
        vacancies_list = [Vacancy(vacancy['name'], vacancy['alternate_url'], vacancy.get('salary'), vacancy.get('snippet').get('responsibility')) for vacancy in hh_vacancies]

        if filter_words:
            filtered_vacancies = filter_vacancies(vacancies_list, filter_words)
        else:
            filtered_vacancies = vacancies_list

        ranged_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)

        sorted_vacancies = sort_vacancies(ranged_vacancies)
        top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
        print_vacancies(top_vacancies)

        input_user = input("Хотите сохранить вакансии в JSON? (y/anything): ").lower()
        if input_user == "y":
            json_saver = JSONSaver('datas/vacancies.json')
            for vacancy in top_vacancies:
                json_saver.add_vacancy(vacancy)
        else:
            print("Вакансии не сохранены.")

    else:
        print("Не удалось получить вакансии. Пожалуйста, проверьте запрос и попробуйте снова.")


if __name__ == "__main__":
    user_interaction()
