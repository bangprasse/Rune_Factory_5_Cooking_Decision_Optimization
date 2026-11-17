import pytest

from src.recipe_resolver import RecipeResolver
from src.recipe import Recipe
from src.exceptions import RecipeResolutionError


def make_resolver(recipes=None, ingredient_types=None, inventory=None):
    return RecipeResolver(
        crafting_recipes=recipes or {},
        ingredient_types=ingredient_types or {},
        inventory=inventory or {},
    )


def test_unknown_ingredient_raises_resolver_error():
    resolver = make_resolver(inventory={"Turnip": 5})

    with pytest.raises(RecipeResolutionError, match="Unknown ingredient"):
        resolver.parse_requirement("Unknown Item")


def test_unknown_type_raises_resolver_error():
    resolver = make_resolver(
        inventory={"Turnip": 5},
        ingredient_types={"Turnip": "Vegetable"},
    )

    with pytest.raises(RecipeResolutionError, match="Unknown ingredient type"):
        resolver.parse_requirement("type:Unknown Type")


def test_empty_requirement_raises_resolver_error():
    resolver = make_resolver()

    with pytest.raises(RecipeResolutionError, match="cannot be empty"):
        resolver.parse_requirement("")


def test_empty_type_requirement_raises_resolver_error():
    resolver = make_resolver()

    with pytest.raises(RecipeResolutionError, match="Ingredient type cannot be empty"):
        resolver.parse_requirement("type:")


def test_crafting_cycle_reports_full_path():
    recipes = {
        "Apple Jam": Recipe("Apple Jam", ["Grape Jam"]),
        "Grape Jam": Recipe("Grape Jam", ["Strawberry Jam"]),
        "Strawberry Jam": Recipe("Strawberry Jam", ["Grape Jam"]),
    }

    resolver = make_resolver(
        recipes=recipes,
        inventory={"Apple": 5},
    )

    with pytest.raises(
        RecipeResolutionError,
        match=r"Grape Jam -> Strawberry Jam -> Grape Jam",
    ):
        resolver.resolve_requirements(["Apple Jam"])


def test_valid_nested_crafting_resolves():
    recipes = {
        "Apple Jam": Recipe("Apple Jam", ["Apple"]),
    }

    resolver = make_resolver(
        recipes=recipes,
        inventory={"Apple": 5},
    )

    requirements = resolver.resolve_requirements(["Apple Jam"])

    assert requirements[0].ingredient_name == "Apple Jam"
    assert requirements[0].crafting_option is not None
    assert requirements[0].crafting_option.ingredients[0].ingredient_name == "Apple"
