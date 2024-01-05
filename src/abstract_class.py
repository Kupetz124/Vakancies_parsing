from abc import ABC, abstractmethod


class Parser(ABC):
    """
    Абстрактный класс для создания классов-парсеров по API.
    """

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get_vacancies(self):
        pass

    @abstractmethod
    def get_dict(self):
        pass
