from ingredient import Ingredient
from recipe import Recipe
from menu import Menu
import data_loader as dl
from recipe_resolver import IngredientRequirement, CraftingOption, RecipeResolver
import config
from optimizer import BasicOptimizer

menu_prices = {"dish_a": 500, "dish_b": 800, "dish_c": 300}

menu_ingredients = {
    "dish_a": {"rice": 1, "egg": 1},
    "dish_b": {"rice": 2, "milk": 1},
    "dish_c": {"flour": 1, "egg": 1},
}

inventory = {"rice": 5, "egg": 3, "milk": 2, "flour": 4}

optimizer = BasicOptimizer(
    menu_prices=menu_prices,
    target_dishes=3,
    menu_ingredients=menu_ingredients,
    inventory=inventory,
)

result = optimizer.solve()

print(result)
