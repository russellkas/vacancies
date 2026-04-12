from __future__ import annotations

from flask import Flask, flash, redirect, render_template, request, url_for

from src.job import HeadHunterAPI
from src.json import JSONSaver
from src.utils import (
    filter_vacancies,
    get_top_vacancies,
    get_vacancies_by_salary,
    parse_salary_range,
    parse_top_n,
    sort_vacancies,
)
from src.vacancy import Vacancy


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-secret-key"

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.post("/search")
    def search():
        query = request.form.get("query", "").strip()
        raw_top_n = request.form.get("top_n", "10").strip()
        raw_salary_range = request.form.get("salary_range", "0-10000000").strip()
        raw_keywords = request.form.get("keywords", "").strip()

        if not query:
            flash("Введите поисковый запрос.")
            return redirect(url_for("index"))

        top_n = parse_top_n(raw_top_n)
        if top_n is None:
            flash("Поле Top N должно быть положительным числом.")
            return redirect(url_for("index"))

        salary_range = parse_salary_range(raw_salary_range)
        if salary_range is None:
            flash("Диапазон зарплат должен быть в формате min-max.")
            return redirect(url_for("index"))

        hh_api = HeadHunterAPI()
        hh_vacancies = hh_api.get_vacancies(query)

        vacancies_list = [
            Vacancy(
                vacancy["name"],
                vacancy["alternate_url"],
                vacancy.get("salary"),
                vacancy.get("snippet", {}).get("responsibility"),
                vacancy.get("employer", {}).get("name"),
            )
            for vacancy in hh_vacancies
        ]

        keywords = [word for word in raw_keywords.split() if word]
        if keywords:
            vacancies_list = filter_vacancies(vacancies_list, keywords)

        ranged_vacancies = get_vacancies_by_salary(vacancies_list, salary_range)
        sorted_vacancies = sort_vacancies(ranged_vacancies)
        top_vacancies = get_top_vacancies(sorted_vacancies, top_n)

        if top_vacancies and isinstance(top_vacancies[0], Vacancy):
            saver = JSONSaver("datas/vacancies.json")
            for vacancy in top_vacancies:
                saver.add_vacancy(vacancy)

        return render_template(
            "index.html",
            vacancies=top_vacancies,
            query=query,
            top_n=raw_top_n,
            salary_range=raw_salary_range,
            keywords=raw_keywords,
        )

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
