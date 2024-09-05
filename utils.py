import os
from typing import NoReturn, Tuple, Callable, Optional


class Menu:
    def __init__(self, options: list[Tuple[str, Optional[Callable[[], NoReturn]]]], title=""):
        self.selected_option = None
        self.options = options
        self.title = title or None

    @staticmethod
    def validate_selected_option(selected_option: str, max_options: int) -> bool:
        if selected_option.isdigit():
            if 0 < int(selected_option) <= max_options:
                return True
            else:
                return False
        else:
            return False

    def render(self, selected_option=-1, updated_options=None):
        os.system('cls||clear')
        if self.title:
            print('\n' + self.title + '\n')
        options = updated_options or self.options

        i = 0
        while i < len(options):
            print(f'[{i + 1}] {options[i][0]}')
            if int(selected_option) == i + 1:
                if not (options[i][1] is None):
                    options[i][1]()
            i += 1

        user_selected_option = input('\nВыберите опцию: ')
        if self.validate_selected_option(user_selected_option, len(options)):
            self.render(int(user_selected_option))
        else:
            self.render()


class Search:
    def __init__(self):
        self.user_input_name = None
        self.user_input_categories = None
        self.user_input_proteins = None
        self.user_input_carbohydrates = None
        self.user_input_fats = None
        self.user_input_calories = None
        self.selected_option = None


class Search_Recipes(Search):
    def __init__(self):
        super().__init__()
        self.user_input_ingredients = None
        self.user_input_cooking_speed = None


def create_recipe_card(data: dict) -> str:
    return f"\tНазвание: {data.get('name')}\n" \
           f"\tКатегория: {data.get('category')}\n" \
           f"\tВремя приготовления: {data.get('cooking_speed')}\n" \
           f"\tИнгредиенты: {data.get('ingredients')}\n" \
           f"\tКалории на 100г: {data.get('calories')}\n" \
           f"\tБелки на 100г: {data.get('proteins')}\n" \
           f"\tУглвеоды на 100г: {data.get('carbohydrates')}\n" \
           f"\tЖиры на 100г: {data.get('fats')}\n"


class Pagination:
    def __init__(self, data: list[dict], offset: int, limit: int):
        self.data = data
        self.offset = offset
        self.limit = limit
        self.paginate_data = self.pagination()

    def pagination(self) -> list:
        return self.data[self.offset:][:self.limit]

    def next(self) -> NoReturn:
        if not self.offset + self.limit + 1 > len(self.data):
            self.offset += self.limit
        self.paginate_data = self.pagination()

    def prev(self):
        if self.offset - self.limit + 1 < 0:
            self.offset = 0
        else:
            self.offset -= self.limit

        self.paginate_data = self.pagination()
