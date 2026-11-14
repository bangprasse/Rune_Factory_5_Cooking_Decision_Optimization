from ingredient import Ingredient
from recipe import Recipe
from menu import Menu
import data_loader as dl
from recipe_resolver import IngredientRequirement, CraftingOption, RecipeResolver
import config
from optimizer import BasicOptimizer

menu_prices = {"dish_a": 500, "dish_b": 800, "dish_c": 300}

optimizer = BasicOptimizer(menu_prices=menu_prices, target_dishes=10)

result = optimizer.solve()

print(result)
