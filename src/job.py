from src.abstract import AbstractVacancyAPI
import requests


class HeadHunterAPI(AbstractVacancyAPI):
    def __init__(self):
        self.url = 'https://api.hh.ru/vacancies'

    def get_vacancies(self, search_query):
        params = {
            'text': search_query,
            'per_page': 100
        }
        try:
            response = requests.get(self.url, params=params, timeout=10)
            response.raise_for_status()
            return response.json().get('items', [])
        except requests.exceptions.RequestException:
            return []

        
