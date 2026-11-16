from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data directory
DATA_DIR = PROJECT_ROOT / "data"

# Dataset paths
CONFIG_PATH = DATA_DIR / "config.csv"
INVENTORY_PATH = DATA_DIR / "inventory.csv"
MENUS_PATH = DATA_DIR / "menus.csv"
CRAFTING_RECIPES_PATH = DATA_DIR / "crafting_recipes.csv"
INGREDIENT_TYPES_PATH = DATA_DIR / "ingredient_types.csv"
