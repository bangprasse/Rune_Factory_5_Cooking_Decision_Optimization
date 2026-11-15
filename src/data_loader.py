import csv
import recipe as rc
from menu import Menu


def load_inventory(filepath):
    inventory = {}

    with open(filepath, "r", newline="", encoding="UTF-8") as file:
        reader = csv.DictReader(file)

        # check required columns
        required_columns = {"ingredient", "quantity"}

        if not required_columns.issubset(reader.fieldnames or []):
            raise ValueError(
                "inventory.csv must contain " "'ingredient' and 'quantity' columns"
            )

        # Read each row
        for row in reader:
            ingredient = row["ingredient"].strip()
            quantity_text = row["quantity"].strip()

            # check empty values
            if not ingredient or not quantity_text:
                raise ValueError("ingredient name and quantity cannot be empty")

            # Check duplicate ingredients
            if ingredient in inventory:
                raise ValueError(f"Duplicate ingredient in inventory: {ingredient!r}")

            # Convert quantity to integer
            try:
                quantity = int(quantity_text)
            except ValueError:
                raise ValueError(
                    f"Invalid quantitiy for {ingredient!r}: {quantity_text!r}"
                )

            # Check negative quantity
            if quantity < 0:
                raise ValueError(f"Quantitiy cannot be negative: {ingredient!r}")

            # Store to inventory
            inventory[ingredient] = quantity

    return inventory


def load_ingredient_types(filepath):
    ingredient_types = {}

    with open(filepath, "r", newline="", encoding="UTF-8") as file:
        reader = csv.DictReader(file)

        # Check required columns
        required_columns = {"ingredient", "type"}

        if not required_columns.issubset(reader.fieldnames or []):
            raise ValueError(
                "ingredient_types.csv must contain 'ingredient' and 'type' columns"
            )

        # Read each row
        for row in reader:
            ingredient = row["ingredient"].strip()
            ingredient_type = row["type"].strip()

            # Check empty values
            if not ingredient or not ingredient_type:
                raise ValueError("ingredient name and type cannot be empty")

            # Check duplicate ingredients
            if ingredient in ingredient_types:
                raise ValueError(
                    f"Duplicate ingredient in ingredient mapping: {ingredient}"
                )

            # Store to ingredient_types
            ingredient_types[ingredient] = ingredient_type

    return ingredient_types


def load_crafting_recipes(filepath):
    recipes = {}

    with open(filepath, "r", newline="", encoding="UTF-8") as file:
        reader = csv.DictReader(file)

        # Check required column
        required_columns = {"product", "ingredients"}

        if not required_columns.issubset(reader.fieldnames or []):
            raise ValueError(
                "crafting_recipes.csv must contain 'product' and 'ingredients' columns"
            )

        # Read each row
        for row in reader:
            product = row["product"].strip()
            ingredients_text = row["ingredients"].strip()

            # Check empty values
            if not product or not ingredients_text:
                raise ValueError("Product name and ingredients cannot be empty")

            # Check duplicate products
            if product in recipes:
                raise ValueError(f"Duplicate crafting recipe: {product}")

            # Split ingredients using +
            ingredients = [
                ingredient.strip() for ingredient in ingredients_text.split("+")
            ]

            # Check for empty ingredient tokens
            if any(not ingredient for ingredient in ingredients):
                raise ValueError(f"Invalid ingredient list for {product}")

            # Create Recipe object
            recipe = rc.Recipe(product, ingredients)

            # Store to recipes
            recipes[product] = recipe

    return recipes


def load_menus(filepath):
    menus = {}

    with open(filepath, "r", newline="", encoding="UTF-8") as file:
        reader = csv.DictReader(file)

        # Check required column
        required_columns = {"menu", "level", "sellprice", "equipment", "ingredients"}

        if not required_columns.issubset(reader.fieldnames or []):
            raise ValueError(
                "menus.csv must contain 'menu', 'level', 'sellprice', 'equipment' and 'ingredients'"
            )

        # Read each row
        for row in reader:
            menu_name = row["menu"].strip()
            level_text = row["level"].strip()
            price_text = row["sellprice"].strip()
            equip_text = row["equipment"].strip()
            ingredients_text = row["ingredients"].strip()

            # Check empty values
            if (
                not menu_name
                or not level_text
                or not price_text
                or not equip_text
                or not ingredients_text
            ):
                raise ValueError(
                    f"Menu name, level, sellprice, equipment and ingredients cannot be empty"
                )

            # Check duplicate menus
            if menu_name in menus:
                raise ValueError(f"Duplicate menu: {menu_name!r}")

            # Convert to integer for level and sellprice
            try:
                cooking_level = int(level_text)
                sell_price = int(price_text)
            except ValueError:
                raise ValueError(f"Invalid level or sell price for menu: {load_menus}")

            # Check negative value for level and sellprice
            if cooking_level < 0 or sell_price < 0:
                raise ValueError(f"Level and sell price for menu: {menu_name}")

            # Split ingredient using +
            ingredients = [
                ingredient.strip() for ingredient in ingredients_text.split("+")
            ]

            # Check for empty ingredient tokens
            if any(not ingredient for ingredient in ingredients):
                raise ValueError(f"Invalid ingredient list for {menu_name}")

            # Create Recipe object
            recipe = rc.Recipe(menu_name, ingredients)

            # Create Menu object
            menu = Menu(
                name=menu_name,
                recipe=recipe,
                sell_price=sell_price,
                cooking_level=cooking_level,
            )

            # Store to menus
            menus[menu_name] = menu

    return menus


def load_config(filepath):
    config = {}

    with open(filepath, "r", newline="", encoding="UTF-8") as file:
        reader = csv.DictReader(file)

        # Check required column
        required_columns = {"setting", "value"}

        if not required_columns.issubset(reader.fieldnames or []):
            raise ValueError('config.csv must contain "setting" and "value"')

        # Read each row
        for row in reader:
            setting = row["setting"].strip()
            value = row["value"].strip()

            # Check empty value
            if not setting or not value:
                raise ValueError("Config setting and value cannot be empty")

            # Check duplicate setting
            if setting in config:
                raise ValueError(f"Duplicate configuration setting: {setting}")

            # Store to config
            config[setting] = value

    return config


def build_type_members(ingredient_types):
    type_members = {}

    for ingredient, ingredient_type in ingredient_types.items():
        if ingredient_type not in type_members:
            type_members[ingredient_type] = []

        type_members[ingredient_type].append(ingredient)

    return type_members
