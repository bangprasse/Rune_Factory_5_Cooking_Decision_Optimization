from ingredient import Ingredient
from recipe import Recipe
from menu import Menu
import data_loader as dl
from recipe_resolver import IngredientRequirement, CraftingOption, RecipeResolver
import config

inventory = dl.load_inventory(config.INVENTORY_PATH)
crafting_recipes = dl.load_crafting_recipes(config.CRAFTING_RECIPES_PATH)
ingredient_types = dl.load_ingredient_types(config.INGREDIENT_TYPES_PATH)
menus = dl.load_menus(config.MENUS_PATH)

resolver = RecipeResolver(crafting_recipes, ingredient_types, inventory)

menu_name, menu = next(iter(menus.items()))

resolved_ingredients = resolver.resolve_requirements(menu.recipe.ingredients)

print("Menu:", menu_name)

for ingredient in resolved_ingredients:
    print(ingredient)

errors = []

for product_name, recipe in crafting_recipes.items():
    try:
        resolver.resolve_crafting_option(resolver.parse_requirement(product_name))
    except ValueError as error:
        errors.append(f"Recipe '{product_name}': {error}")

print("Crafting recipes checked:", len(crafting_recipes))
print("Errors:", len(errors))

for error in errors:
    print(error)
