from dataclasses import dataclass, field
from src.exceptions import RecipeResolutionError


@dataclass
class IngredientRequirement:
    ingredient_name: str
    quantity: int = 1
    requirement_type: str = "specific"
    crafting_option: "CraftingOption | None" = None


@dataclass
class CraftingOption:
    product_name: str
    ingredients: list[IngredientRequirement] = field(default_factory=list)


class RecipeResolver:
    """Parses and validates ingredient requirements."""

    def __init__(self, crafting_recipes, ingredient_types, inventory):
        self.crafting_recipes = crafting_recipes
        self.ingredient_types = ingredient_types
        self.inventory = inventory

        # Ingredients that are known to the application
        self.known_ingredients = (
            set(inventory.keys())
            | set(crafting_recipes.keys())
            | set(ingredient_types.keys())
        )

        # All valid ingredient types
        self.known_types = set(ingredient_types.values())

    def parse_requirement(self, token):
        """Convert a requirement token into an IngredienRequirement"""

        # Remove whitespace around the token
        token = token.strip()

        # Reject empty requirements
        if not token:
            raise RecipeResolutionError("Ingredient requirement cannot be empty")

        # Handle ingredient-type requirement
        if token.startswith("type:"):
            type_name = token[len("type:") :].strip()

            if not type_name:
                raise RecipeResolutionError("Ingredient type cannot be empty")

            if type_name not in self.known_types:
                raise RecipeResolutionError(f"Unknown ingredient type: {type_name!r}")

            return IngredientRequirement(
                ingredient_name=type_name, quantity=1, requirement_type="type"
            )

        # Handle spesific ingredient requirements
        if token not in self.known_ingredients:
            raise RecipeResolutionError(f"Unknown ingredient: {token!r}")

        return IngredientRequirement(
            ingredient_name=token, quantity=1, requirement_type="specific"
        )

    def attach_crafting_option(self, requirement):
        """Attach a crafting recipe when one exists"""

        # Type requirements cannot be directly crafted
        if requirement.requirement_type == "type":
            return requirement

        # check whether this ingredient has a crafting recipe
        if requirement.ingredient_name not in self.crafting_recipes:
            return requirement

        # Retrieve the crafting recipe
        recipe = self.crafting_recipes[requirement.ingredient_name]

        # Convert its ingredients into requirements
        crafting_ingredients = []

        for ingredient in recipe.ingredients:
            crafting_ingredients.append(self.parse_requirement(ingredient))

        # Create the crafting alternative
        requirement.crafting_option = CraftingOption(
            product_name=requirement.ingredient_name, ingredients=crafting_ingredients
        )

        return requirement

    def resolve_crafting_option(self, requirement, path=None):
        """Recursively attach crafting alternatives with cycle detection."""
        if path is None:
            path = ()

        # Type requirements cannot have direct crafting recipes
        if requirement.requirement_type == "type":
            return requirement

        ingredient_name = requirement.ingredient_name

        # Detect and report the complete crafting cycle
        if ingredient_name in path:
            cycle_start = path.index(ingredient_name)
            cycle = path[cycle_start:] + (ingredient_name,)
            cycle_path = " -> ".join(cycle)

            raise RecipeResolutionError(f"Crafting cycle detected: {cycle_path}")

        # No crafting recipe exists for this ingredient
        if ingredient_name not in self.crafting_recipes:
            return requirement

        current_path = path + (ingredient_name,)
        recipe = self.crafting_recipes[ingredient_name]

        crafting_ingredients = []

        for ingredient in recipe.ingredients:
            child_requirement = self.parse_requirement(ingredient)

            child_requirement = self.resolve_crafting_option(
                child_requirement,
                current_path,
            )

            crafting_ingredients.append(child_requirement)

        requirement.crafting_option = CraftingOption(
            product_name=ingredient_name,
            ingredients=crafting_ingredients,
        )

        return requirement

    def resolve_requirements(self, ingredients):
        """Parse and recursively resolve a list of ingredient requirements"""

        resolved_requirements = []

        for ingredient in ingredients:
            requirement = self.parse_requirement(ingredient)

            requirement = self.resolve_crafting_option(requirement)

            resolved_requirements.append(requirement)

        return resolved_requirements
