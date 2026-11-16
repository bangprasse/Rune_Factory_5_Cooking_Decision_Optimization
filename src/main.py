from ingredient import Ingredient
from recipe import Recipe
from menu import Menu
import data_loader as dl
from recipe_resolver import IngredientRequirement, CraftingOption, RecipeResolver
import config
from optimizer import BasicOptimizer
from result import OptimizationResult

result = OptimizationResult(
    status="OPTIMAL",
    player_cooking_level=50,
    target_dish_count=10,
    selected_menus={
        "seafood_doria": {"quantity": 3, "equipment": "oven"},
        "omelet": {"quantity": 2, "equipment": "frying_pan"},
        "grilled_shrimp": {"quantity": 5, "equipment": "frying_pan"},
    },
    total_dishes=10,
    total_revenue=25000,
    total_rp=120,
    ingredient_usage={
        "rice": 3,
        "shrimp": 3,
        "dairy": 6,
    },
    remaining_inventory={
        "rice": 7,
        "shrimp": 2,
        "dairy": 4,
    },
)

print(result.status)
print(result.selected_menus)
print(result.total_revenue)
