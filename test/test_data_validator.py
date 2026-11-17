from src.data_validator import validate_data
from src.recipe import Recipe
from src.menu import Menu


def create_test_menu(name, ingredients):
    recipe = Recipe(name, ingredients)

    return Menu(
        name=name,
        recipe=recipe,
        sell_price=100,
        cooking_level=1,
        rp=0,
        equipment="knife",
    )


def test_valid_data():
    inventory = {"apple": 5}
    recipes = {}
    ingredient_types = {"apple": "fruit"}
    menus = {
        "apple_dish": create_test_menu(
            "apple_dish",
            ["apple"],
        )
    }

    result = validate_data(
        inventory,
        recipes,
        ingredient_types,
        menus,
    )

    assert result.is_valid
    assert result.errors == []


def test_unknown_ingredient():
    inventory = {}
    recipes = {}
    ingredient_types = {}
    menus = {
        "apple_dish": create_test_menu(
            "apple_dish",
            ["unknown_ingredient"],
        )
    }

    result = validate_data(
        inventory,
        recipes,
        ingredient_types,
        menus,
    )

    assert not result.is_valid
    assert any("unknown_ingredient" in error for error in result.errors)


def test_unknown_ingredient_type():
    inventory = {}
    recipes = {}
    ingredient_types = {}
    menus = {
        "fruit_dish": create_test_menu(
            "fruit_dish",
            ["type:fruit"],
        )
    }

    result = validate_data(
        inventory,
        recipes,
        ingredient_types,
        menus,
    )

    assert not result.is_valid
    assert any("fruit" in error for error in result.errors)


def test_multiple_errors():
    inventory = {}
    recipes = {}
    ingredient_types = {}
    menus = {
        "test_dish": create_test_menu(
            "test_dish",
            ["bad_ingredient", "type:bad_type"],
        )
    }

    result = validate_data(
        inventory,
        recipes,
        ingredient_types,
        menus,
    )

    assert not result.is_valid
    assert len(result.errors) == 2


def test_real_project_data():
    from src.data_loader import (
        load_inventory,
        load_ingredient_types,
        load_crafting_recipes,
        load_menus,
    )
    from src.data_validator import validate_data
    import src.config as config

    inventory = load_inventory(config.INVENTORY_PATH)
    ingredient_types = load_ingredient_types(config.INGREDIENT_TYPES_PATH)
    recipes = load_crafting_recipes(config.CRAFTING_RECIPES_PATH)
    menus = load_menus(config.MENUS_PATH)

    result = validate_data(
        inventory,
        recipes,
        ingredient_types,
        menus,
    )

    assert result.is_valid, result.errors


from src.data_validator import detect_recipe_cycles


def test_no_recipe_cycle():
    recipes = {
        "flour": Recipe("flour", ["wheat"]),
        "bread": Recipe("bread", ["flour"]),
    }

    errors = detect_recipe_cycles(recipes)

    assert errors == []


def test_recipe_cycle():
    recipes = {
        "recipe_a": Recipe("recipe_a", ["recipe_b"]),
        "recipe_b": Recipe("recipe_b", ["recipe_a"]),
    }

    errors = detect_recipe_cycles(recipes)

    assert len(errors) > 0
    assert any("cycle" in error.lower() for error in errors)


def test_self_recipe_cycle():
    recipes = {
        "recipe_a": Recipe("recipe_a", ["recipe_a"]),
    }

    errors = detect_recipe_cycles(recipes)

    assert len(errors) > 0
