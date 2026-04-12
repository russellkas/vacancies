import re

class Vacancy:
    name: str
    link: str
    salary: dict
    description: str

    def __init__(self, title, link, salary, description, employer):
        self.title = title
        self.link = link
        self.salary = salary.get('from') if salary and salary.get('from') else 0
        self.description = self._clean_description(description)        
        self.employer = employer if employer else "Employer"

    def __str__(self):
        return f"Title: {self.title}\nLink: {self.link}\nSalary: {self.salary}\nEmployer: {self.employer}\nDescription: {self.description}"

    def __lt__(self, other):
        return self.salary < other.salary

    def __eq__(self, other):
        return self.salary == other.salary
    
    @staticmethod
    def _clean_description(description):
        if not description:
            return "Описание отсутствует"

        return re.sub(r"</?highlighttext>", "", description, flags=re.IGNORECASE)



