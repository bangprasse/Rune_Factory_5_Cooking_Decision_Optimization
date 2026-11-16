from ingredient import Ingredient
from recipe import Recipe
from menu import Menu
import data_loader as dl
from recipe_resolver import IngredientRequirement, CraftingOption, RecipeResolver
import config
from optimizer import BasicOptimizer
from result import OptimizationResult
from collections import Counter

# Load config
settings = dl.load_config(config.CONFIG_PATH)
player_cooking_level = int(settings["player_cooking_level"])
target_dish_count = int(settings["target_dish_count"])

# Load menus
menus = dl.load_menus(config.MENUS_PATH)

# Prepare optimizer input dictionaries
menu_prices = {}
menu_ingredients = {}
menu_rp = {}
menu_equipments = {}

# Filter menus by player cooking level
for menu_name, menu in menus.items():
    if menu.cooking_level > player_cooking_level:
        continue

    # Menu selling price
    menu_prices[menu_name] = menu.sell_price

    # Count ingredients requirement
    menu_ingredients[menu_name] = dict(Counter(menu.recipe.ingredients))

    # Preserve rp and equipment for reporting
    menu_rp[menu_name] = menu.rp
    menu_equipments[menu_name] = menu.equipment

# Load crafting recipes
recipes = dl.load_crafting_recipes(config.CRAFTING_RECIPES_PATH)

# Convert crafting recipes into optimizer format
crafting_recipes = {}

for product_name, recipe in recipes.items():
    crafting_recipes[product_name] = dict(Counter(recipe.ingredients))

# Load inventory
inventory = dl.load_inventory(config.INVENTORY_PATH)

# Load ingredient types
ingredient_types = dl.load_ingredient_types(config.INGREDIENT_TYPES_PATH)

# Build ingredient type membership
type_members = dl.build_type_members(ingredient_types)


# Create optimizer
optimizer = BasicOptimizer(
    menu_prices=menu_prices,
    target_dishes=target_dish_count,
    menu_ingredients=menu_ingredients,
    inventory=inventory,
    crafting_recipes=crafting_recipes,
    type_members=type_members,
)

# Solve optimization problem
optimization = optimizer.solve()

# Prepare selected menus for OptimizationResult
selected_menus = {}

for menu_name, quantity in optimization["menu_quantities"].items():
    selected_menus[menu_name] = {
        "quantity": quantity,
        "equipment": menu_equipments[menu_name],
    }

# Calculate total RP
total_rp = sum(
    quantity * menu_rp[menu_name]
    for menu_name, quantity in optimization["menu_quantities"].items()
)

# Create OptimizationResult
result = OptimizationResult(
    status=optimization["status"],
    player_cooking_level=player_cooking_level,
    target_dish_count=target_dish_count,
    selected_menus=selected_menus,
    total_dishes=optimization["total_dishes"],
    total_revenue=optimization["total_revenue"],
    total_rp=total_rp,
    ingredient_usage=optimization["ingredient_consumption"],
    remaining_inventory=optimization["remaining_inventory"],
    crafted_quantities=optimization["crafted_quantities"],
)

result.display()
