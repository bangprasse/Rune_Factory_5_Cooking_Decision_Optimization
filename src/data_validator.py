from dataclasses import dataclass


@dataclass
class ValidationResult:
    errors: list[str]
    warnings: list[str]

    @property
    def is_valid(self) -> bool:
        return len(self.errors) == 0


def validate_data(
    inventory,
    recipes,
    ingredient_types,
    menus,
) -> ValidationResult:
    errors = []
    warnings = []

    # All concrete ingredients known to the application
    known_ingredients = (
        set(inventory.keys()) | set(recipes.keys()) | set(ingredient_types.keys())
    )

    # All available ingredient types
    known_types = set(ingredient_types.values())

    def validate_requirements(owner_name, ingredients):
        for ingredient in ingredients:

            if ingredient.startswith("type:"):
                ingredient_type = ingredient.removeprefix("type:")

                if ingredient_type not in known_types:
                    errors.append(
                        f"{owner_name} references unknown "
                        f"ingredient type: {ingredient_type!r}"
                    )

            elif ingredient not in known_ingredients:
                errors.append(
                    f"{owner_name} references unknown " f"ingredient: {ingredient!r}"
                )

    # Validate crafting recipe ingredient references
    for product, recipe in recipes.items():
        validate_requirements(
            f"Crafting recipe {product!r}",
            recipe.ingredients,
        )

    # Validate menu ingredient references
    for menu_name, menu in menus.items():
        validate_requirements(
            f"Menu {menu_name!r}",
            menu.recipe.ingredients,
        )

    errors.extend(detect_recipe_cycles(recipes))

    return ValidationResult(
        errors=errors,
        warnings=warnings,
    )


def detect_recipe_cycles(recipes):
    """Detect circular dependencies between crafting recipes."""

    errors = []
    visited = set()
    active_path = set()

    def visit(product):
        if product in active_path:
            errors.append(f"Recipe cycle detected involving '{product}'")
            return

        if product in visited:
            return

        active_path.add(product)

        recipe = recipes[product]

        for ingredient in recipe.ingredients:
            if ingredient in recipes:
                visit(ingredient)

        active_path.remove(product)
        visited.add(product)

    for product in recipes:
        visit(product)

    return errors
