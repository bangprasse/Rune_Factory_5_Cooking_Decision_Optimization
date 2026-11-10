from ingredient import Ingredient
from recipe import Recipe
from menu import Menu
import data_loader as dl

inventory = dl.load_inventory("../data/inventory.csv")
ingredient_types = dl.load_ingredient_types("../data/ingredient_types.csv")
recipes = dl.load_crafting_recipes("../data/crafting_recipes.csv")
menus = dl.load_menus("../data/menus.csv")
config = dl.load_config("../data/config.csv")


# Check that all datasets loaded
assert len(inventory) > 0
assert len(ingredient_types) > 0
assert len(recipes) > 0
assert len(menus) > 0
assert len(config) > 0

# Check data structures
assert isinstance(inventory, dict)
assert isinstance(ingredient_types, dict)
assert isinstance(recipes, dict)
assert isinstance(menus, dict)
assert isinstance(config, dict)

# Check object types
assert isinstance(next(iter(recipes.values())), Recipe)
assert isinstance(next(iter(menus.values())), Menu)

# Display dataset sizes
print("Combined data loading test passed!")
print(f"Inventory items: {len(inventory)}")
print(f"Ingredient type mappings: {len(ingredient_types)}")
print(f"Crafting recipes: {len(recipes)}")
print(f"Menus: {len(menus)}")
print(f"Config settings: {len(config)}")
