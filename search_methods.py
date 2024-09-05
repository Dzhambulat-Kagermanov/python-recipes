from typing import Tuple, Optional


class Search_Methods:
    def __init__(self, name: Optional[str], categories: Optional[list[str]], proteins: Optional[Tuple[int, int]],
                 carbohydrates: Optional[Tuple[int, int]], fats: Optional[Tuple[int, int]],
                 calories: Optional[Tuple[int, int]]):
        self.name = name
        self.categories = categories
        self.nutritional_value = {
            "proteins": proteins,
            "carbohydrates": carbohydrates,
            "fats": fats,
            "calories": calories
        }

    def name_validation(self, data_name: str) -> bool:
        if not self.name:
            return True

        return self.name in data_name

    def categories_validation(self, data_category: str) -> bool:
        if not self.categories:
            return True

        i = 0
        result = False
        while i < len(self.categories):
            if self.categories[i].lower() == data_category.lower():
                result = True
                i = len(self.categories)
            i += 1

        return result

    @staticmethod
    def range_validation(val_range, data_range: float) -> bool:
        if str(val_range[0]).isdigit() or str(val_range[1]).isdigit():
            if val_range[0] > val_range[1]:
                return False
            elif val_range[0] <= data_range <= val_range[1]:
                return True

            return False
        else:
            return False

    def nutritional_validation(self, data_proteins: float, data_carbohydrates: float, data_fats: float,
                               data_calories: float) -> bool:

        proteins = True if not (self.nutritional_value.get('proteins') or self.nutritional_value.get(
            'proteins') == 0) else self.range_validation(
            self.nutritional_value.get('proteins'), data_proteins)
        carbohydrates = True if not (self.nutritional_value.get('carbohydrates') or self.nutritional_value.get(
            'carbohydrates') == 0) else self.range_validation(
            self.nutritional_value.get('carbohydrates'), data_carbohydrates)
        fats = True if not (self.nutritional_value.get('fats') or self.nutritional_value.get(
            'fats') == 0) else self.range_validation(
            self.nutritional_value.get('fats'), data_fats)
        calories = True if not (self.nutritional_value.get('calories') or self.nutritional_value.get(
            'calories') == 0) else self.range_validation(
            self.nutritional_value.get('calories'), data_calories)

        if proteins and carbohydrates and fats and calories:
            return True

        return False

    def search_validation(self, data: dict) -> bool:
        name = self.name_validation(data.get("name"))
        nutritional = self.nutritional_validation(data_proteins=data.get('proteins'), data_fats=data.get('fats'),
                                                  data_calories=data.get('calories'),
                                                  data_carbohydrates=data.get('carbohydrates'))
        category = self.categories_validation(data.get('category'))

        if name and nutritional and category:
            return True

        return False


class Search_Methods_Recipes(Search_Methods):
    def __init__(self, name: Optional[str], categories: Optional[list[str]], proteins: Optional[Tuple[int, int]],
                 carbohydrates: Optional[Tuple[int, int]], fats: Optional[Tuple[int, int]],
                 calories: Optional[Tuple[int, int]], ingredients: Optional[list[str]],
                 cooking_speed: Optional[Tuple[int, int]]):
        super().__init__(name=name, calories=calories, categories=categories, proteins=proteins,
                         carbohydrates=carbohydrates, fats=fats)
        self.ingredients = list(map(lambda el: el.lower(), ingredients)) if ingredients else []
        self.cooking_speed = cooking_speed

    def cooking_speed_validation(self, data_cooking_speed: int):
        return self.range_validation(self.cooking_speed, data_cooking_speed)

    def search_combine(self, data: list[dict]) -> list[dict]:
        global ingredients_is_valid
        result = []
        for val in data:
            other_values_validation = self.search_validation(val)
            cooking_speed = True if not self.cooking_speed else self.cooking_speed_validation(
                val.get('cooking_speed'))
            ingredients_is_valid = False
            data_ingredients = list(map(lambda el: el.lower(), val.get('ingredients').split()))

            if not self.ingredients:
                ingredients_is_valid = True
            else:
                global counter
                counter = len(self.ingredients)
                i = 0
                while i < len(self.ingredients):
                    j = 0
                    if counter == 0:
                        break
                    while j < len(data_ingredients):
                        if self.ingredients[i] == data_ingredients[j]:
                            counter -= 1
                        if counter == 0:
                            ingredients_is_valid = True
                            break
                        j += 1
                    i += 1

            if ingredients_is_valid and other_values_validation and cooking_speed:
                result.append(val)
        return result

    def search_strict(self, data: list[dict]) -> list[dict]:
        global ingredients_is_valid

        result = []
        for val in data:
            other_values_validation = self.search_validation(val)
            cooking_speed = True if not self.cooking_speed else self.cooking_speed_validation(
                val.get('cooking_speed'))
            ingredients_is_valid = False

            data_ingredients = map(lambda el: el.lower(), val.get('ingredients').split())

            if not self.ingredients:
                ingredients_is_valid = True
            else:
                ingredients_is_valid = set(self.ingredients) == set(data_ingredients)

            if ingredients_is_valid and other_values_validation and cooking_speed:
                result.append(val)
        return result

    def search_difference(self, data: list[dict]) -> list[dict]:
        global ingredients_is_valid
        result = []
        for val in data:
            other_values_validation = self.search_validation(val)
            cooking_speed = True if not self.cooking_speed else self.cooking_speed_validation(
                val.get('cooking_speed'))

            ingredients_is_valid = True

            data_ingredients = list(map(lambda el: el.lower(), val.get('ingredients').split()))


            if not self.ingredients:
                ingredients_is_valid = True
            else:
                i = 0
                while i < len(self.ingredients):
                    j = 0
                    if data_ingredients[j] == self.ingredients[i]:
                        break
                    while j < len(data_ingredients):
                        print(data_ingredients[j])
                        print(self.ingredients[i])
                        if data_ingredients[j] == self.ingredients[i]:
                            ingredients_is_valid = False
                            break
                        j += 1
                    i += 1
            if other_values_validation and ingredients_is_valid and cooking_speed:
                result.append(val)

        return result
