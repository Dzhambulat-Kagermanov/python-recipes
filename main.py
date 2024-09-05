import json
from utils import *
from search_methods import *
import sys
from typing import Literal


def start_menu():
    menu = Menu(
        [
            ('Поиск', lambda: search_recipes_menu(start_menu)),
            ('Все ингредиенты', lambda: all_products_params_menu(start_menu, type='ingredients')),
            ('Все категории', lambda: all_products_params_menu(start_menu, type='categories')),
            ('Выход', sys.exit)
        ],
        'Поиск кулинарных рецептов по параметрам'
    )
    menu.render()


def search_recipes_menu(back_method: Callable):
    def helper():
        print(
            "\nВсе виды поисков различаются только по поиску по ингредиентам все остальные параметры фильтруются одинакого"
            "\n\tОбъединённый поиск: Кроме указанных ингредиентов рецепт может содержать и другие ингредиенты"
            "\n\tСтрогий поиск: Рецепт может содержать только указанные ингредиенты"
            "\n\tИсключающий поиск: Все рецепты которые не содержат указанные ингредиенты"
        )
        input("\nНазад (Enter): ")
        menu.render()

    menu = Menu(
        [
            ('Назад', back_method),
            ('Объединенный поиск',
             lambda: search_recipes_method_menu('combine', lambda: search_recipes_menu(back_method),
                                                'Объединённый поиск')),
            ('Строгий поиск',
             lambda: search_recipes_method_menu('strict', lambda: search_recipes_menu(back_method), 'Строгий поиск')),
            ('Исключающий поиск',
             lambda: search_recipes_method_menu('difference', lambda: search_recipes_menu(back_method),
                                                'Исключающий поиск')),
            ('Помощь', helper),
        ],
        'Поиск рецептов'
    )
    menu.render()


def search_recipes_method_menu(search_method: Literal['combine', 'strict', 'difference'], back_method: Callable, title):
    def helper():
        print(
            "\nВсе параметры явялются не обязательными. Если не ввести ни один из параметров то поиск вывыдет все рецепты."
            "\n\tНазвание может содеражать как полное название так и подстроку."
            "\n\tНазвания категорий и ингредиентов должны быть указаны полностью без сокращений через пробел"
            "\n\tПоля калории, белки, жиры, углвеводы и скорость приготовления принимаю в себя диапазон чисел ОТ и ДО. Вводить только числа без пробелов и других сиволов"
        )
        input("\nНазад (Enter): ")
        menu.render()

    def ranging_data(reserve_title: str, toggler=False):
        toggler and print(reserve_title + "\n")
        value_from = input('От: ')
        value_to = input('До: ')
        if value_from.isdigit() and value_to.isdigit() and int(value_from) <= int(value_to):
            return int(value_from), int(value_to)
        else:
            os.system('cls||clear')
            ranging_data(reserve_title, toggler=True)

    search_menu = Search_Recipes()
    menu = Menu(
        [
            ('Назад', back_method),
            ('Ввести название',
             lambda: setattr(search_menu, 'user_input_name', input(': '))),
            ('Ввести категории', lambda: setattr(search_menu, 'user_input_categories',
                                                 input('Перечисление через пробел (регистер не важен): ').split())),
            ('Ввести ингредиенты', lambda: setattr(search_menu, 'user_input_ingredients',
                                                   input('Перечисление через пробел (регистер не важен): ').split())),
            ('Ввести скорость готовки',
             lambda: setattr(search_menu, 'user_input_cooking_speed',
                             ranging_data("Некоректный ввод. Ввести скорость готовки"))),
            ('Ввести калории на 100г',
             lambda: setattr(search_menu, 'user_input_calories',
                             ranging_data("Некоректный ввод. Ввести калории на 100г"))),
            ('Ввести белки на 100г',
             lambda: setattr(search_menu, 'user_input_proteins',
                             ranging_data("Некоректный ввод. Ввести белки на 100г"))),
            ('Ввести углвеоды на 100г',
             lambda: setattr(search_menu, 'user_input_carbohydrates',
                             ranging_data("Некоректный ввод. Ввести углвеоды на 100г"))),
            ('Ввести жиры на 100г',
             lambda: setattr(search_menu, 'user_input_fats', ranging_data("Некоректный ввод. Ввести жиры на 100г"))),
            ('Поиск', lambda: search_data_menu(
                {
                    "name": search_menu.user_input_name,
                    "categories": search_menu.user_input_categories,
                    "ingredients": search_menu.user_input_ingredients,
                    "cooking_speed": search_menu.user_input_cooking_speed,
                    "calories": search_menu.user_input_calories,
                    "proteins": search_menu.user_input_proteins,
                    "carbohydrates": search_menu.user_input_carbohydrates,
                    "fats": search_menu.user_input_fats
                }, search_method, lambda: search_recipes_method_menu(search_method, back_method, title)
            )),
            ('Помощь', helper),
        ],
        title
    )
    menu.render()


def search_data_menu(filter_data: dict, search_method: Literal['combine', 'strict', 'difference'],
                     back_method: Callable):
    with open('recipes.json', 'r', encoding='utf-8') as recipes:
        global recipes_data
        recipes_data = json.load(recipes)['recipes']
        recipes.close()

    search_recipes = Search_Methods_Recipes(
        filter_data.get('name'),
        filter_data.get('categories'),
        filter_data.get('proteins'),
        filter_data.get('carbohydrates'),
        filter_data.get('fats'),
        filter_data.get('calories'),
        filter_data.get('ingredients'),
        filter_data.get('cooking_speed'),
    )

    global menu_valid_data
    if search_method == 'combine':
        menu_valid_data = search_recipes.search_combine(recipes_data)
    if search_method == 'strict':
        menu_valid_data = search_recipes.search_strict(recipes_data)
    if search_method == 'difference':
        menu_valid_data = search_recipes.search_difference(recipes_data)

    menu_valid_data = list(
        map(lambda recipe: (create_recipe_card(recipe), lambda: None), menu_valid_data))

    search_pagination = Pagination(menu_valid_data, 0, 10)

    def pagination_helper_next():
        search_pagination.next()
        menu.render(updated_options=[
            ('Назад', back_method),
            ('>>>>>', pagination_helper_next),
            ('<<<<<', pagination_helper_prev),
            *search_pagination.paginate_data
        ])

    def pagination_helper_prev():
        search_pagination.prev()

        menu.render(updated_options=[
            ('Назад', back_method),
            ('>>>>>', pagination_helper_next),
            ('<<<<<', pagination_helper_prev),
            *search_pagination.paginate_data
        ])

    menu = Menu([
        ('Назад', back_method),
        ('>>>>>', pagination_helper_next),
        ('<<<<<', pagination_helper_prev),
        *search_pagination.paginate_data
    ], 'Результаты поиска')
    menu.render()


def all_products_params_menu(back_method: Callable, type: Literal['ingredients', 'categories']):
    with open('./recipes.json', 'r', encoding='utf-8') as recipes_file:
        global recipes_data
        recipes_data = json.load(recipes_file)['recipes']
        recipes_file.close()

    products = set()
    for recipe in recipes_data:
        recipe_products = recipe.get('ingredients').split() if type == 'ingredients' else recipe.get('category')
        if type == 'ingredients':
            for product in recipe_products:
                products.add(product)
        else:
            products.add(recipe_products)

    valid_ingredients = list(map(lambda el: (el, lambda: None), list(products)))

    products_pagination = Pagination(valid_ingredients, 0, 10)

    def pagination_helper_next():
        products_pagination.next()
        menu.render(updated_options=[
            ('Назад', back_method),
            ('>>>>>', pagination_helper_next),
            ('<<<<<', pagination_helper_prev),
            *products_pagination.paginate_data
        ])

    def pagination_helper_prev():
        products_pagination.prev()

        menu.render(updated_options=[
            ('Назад', back_method),
            ('>>>>>', pagination_helper_next),
            ('<<<<<', pagination_helper_prev),
            *products_pagination.paginate_data
        ])

    menu = Menu([
        ('Назад', back_method),
        ('>>>>>', pagination_helper_next),
        ('<<<<<', pagination_helper_prev),
        *products_pagination.paginate_data
    ], 'Все ингредиенты')
    menu.render()


start_menu()
