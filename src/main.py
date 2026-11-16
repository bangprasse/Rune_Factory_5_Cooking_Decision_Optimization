from ingredient import Ingredient
from recipe import Recipe
from menu import Menu
import data_loader as dl
from recipe_resolver import IngredientRequirement, CraftingOption, RecipeResolver
import config
from optimizer import BasicOptimizer

# Menu prices
menu_prices = {"test_squid_dish": 100}

# One squid required per dish
menu_ingredients = {"test_squid_dish": {"type:squid": 1}}

# Available inventory
inventory = {"lamp_squid": 1, "squid": 1, "sunsquid": 0}

# Type mapping
type_members = {"squid": ["lamp_squid", "squid", "sunsquid"]}

# Create optimizer
optimizer = BasicOptimizer(
    menu_prices=menu_prices,
    target_dishes=3,
    menu_ingredients=menu_ingredients,
    inventory=inventory,
    type_members=type_members,
)

# Solve
result = optimizer.solve()

# Display results
assert result["status"] != "Optimal"
assert result["total_dishes"] == 0

print("Squid infeasibility test passed!")
