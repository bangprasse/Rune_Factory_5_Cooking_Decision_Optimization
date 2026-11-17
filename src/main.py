from collections import Counter

import src.data_loader as dl
import src.config as config
from src.optimizer import BasicOptimizer
from src.result import OptimizationResult
from src.exceptions import GameOptimizerError, DataValidationError
from src.data_validator import validate_data


def main():

    # Load and validate config
    settings = dl.load_config(config.CONFIG_PATH)
    settings = dl.validate_config(settings)

    player_cooking_level = settings["player_cooking_level"]
    target_dish_count = settings["target_dish_count"]

    # Load all datasets
    inventory = dl.load_inventory(config.INVENTORY_PATH)

    ingredient_types = dl.load_ingredient_types(config.INGREDIENT_TYPES_PATH)

    recipes = dl.load_crafting_recipes(config.CRAFTING_RECIPES_PATH)

    menus = dl.load_menus(config.MENUS_PATH)

    # Validate dataset integrity
    validation = validate_data(
        inventory,
        recipes,
        ingredient_types,
        menus,
    )

    # Stop startup if validation errors exist
    if validation.errors:
        raise DataValidationError(
            "Dataset validation failed:\n- " + "\n- ".join(validation.errors)
        )

    # Display validation warnings
    for warning in validation.warnings:
        print(f"WARNING: {warning}")
    # Prepare optimizer input dictionaries
    menu_prices = {}
    menu_ingredients = {}
    menu_rp = {}
    menu_equipments = {}

    # Filter menus by player cooking level
    for menu_name, menu in menus.items():
        if menu.cooking_level > player_cooking_level:
            continue

        menu_prices[menu_name] = menu.sell_price
        menu_ingredients[menu_name] = dict(Counter(menu.recipe.ingredients))
        menu_rp[menu_name] = menu.rp
        menu_equipments[menu_name] = menu.equipment

    # Convert crafting recipes into optimizer format
    crafting_recipes = {}

    for product_name, recipe in recipes.items():
        crafting_recipes[product_name] = dict(Counter(recipe.ingredients))

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


def run_application():
    try:
        main()
    except GameOptimizerError as error:
        print(f"\nERROR: {error}")


if __name__ == "__main__":
    run_application()
