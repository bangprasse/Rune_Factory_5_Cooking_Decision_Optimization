from ingredient import Ingredient
from recipe import Recipe
from menu import Menu
import data_loader as dl
from recipe_resolver import IngredientRequirement, CraftingOption, RecipeResolver
import config
from optimizer import BasicOptimizer

ingredient_types = dl.load_ingredient_types(config.INGREDIENT_TYPES_PATH)

type_members = dl.build_type_members(ingredient_types)

print(type_members)

assert type_members["squid"] == ["lamp_squid", "squid", "sunsquid"]

assert "apple_jam" in type_members["jam"]

assert "monarch_mushroom" in type_members["mushroom"]

print("Ingredient type mapping tests passed!")
