import json

import pandas as pd


class Reader:
    def __init__(self, path: str) -> None:
        self.__path = path
        try:
            self.data = self.__read_for_json

            self.df = pd.DataFrame(self.data)
            self.df.index = range(1, len(self.df) + 1)

        except (FileNotFoundError, json.JSONDecodeError):
            self.df = pd.DataFrame()
            self.data = []

    @property
    def __read_for_json(self) -> dict:
        with open(self.__path, mode="r", encoding="utf-8") as file:
            data = json.load(file)

            return data
