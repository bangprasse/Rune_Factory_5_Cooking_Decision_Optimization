import csv
from pathlib import Path

import src.recipe as rc
from src.menu import Menu

from src.exceptions import DataValidationError, ConfigurationError


def _open_csv(filepath):
    """Open a CSV file and convert file/parsing errors into clear messages."""
    try:
        file = open(filepath, "r", newline="", encoding="UTF-8")
    except OSError as exc:
        raise DataValidationError(f"Cannot open CSV file {filepath!s}: {exc}") from exc

    return file


def _validate_columns(reader, filepath, required_columns):
    """Check that a CSV file contains all required columns."""
    actual_columns = set(reader.fieldnames or [])
    misisng_columns = required_columns - actual_columns

    if misisng_columns:
        missing = ", ".join(sorted(misisng_columns))
        raise DataValidationError(f"{filepath}: missing required columns(s): {missing}")


def load_inventory(filepath):
    inventory = {}

    with _open_csv(filepath) as file:
        reader = csv.DictReader(file)

        _validate_columns(reader, filepath, {"ingredient", "quantity"})

        # Read each row
        for row_number, row in enumerate(reader, start=2):
            ingredient = (row.get("ingredient") or "").strip()
            quantity_text = (row.get("quantity") or "").strip()

            # check empty values
            if not ingredient:
                raise DataValidationError(
                    f"{filepath}, row {row_number}: ingredient cannot be empty"
                )

            if not quantity_text:
                raise DataValidationError(
                    f"{filepath}, row {row_number}: quantity cannot be empty"
                    f"for ingredient {ingredient!r}"
                )

            # Check duplicate ingredients
            if ingredient in inventory:
                raise DataValidationError(
                    f"{filepath}, row {row_number}: duplicate ingredient "
                    f"{ingredient!r}"
                )

            # Convert quantity to integer
            try:
                quantity = int(quantity_text)
            except ValueError as exc:
                raise DataValidationError(
                    f"{filepath}, row {row_number}: invalid quantity "
                    f"{quantity_text!r} for ingredient {ingredient!r}; "
                    "expected an integer"
                ) from exc

            # Check negative quantity
            if quantity < 0:
                raise DataValidationError(
                    f"{filepath}, row {row_number}: quantity cannot be negative "
                    f"for ingredient {ingredient!r}"
                )

            # Store to inventory
            inventory[ingredient] = quantity

    return inventory


def load_ingredient_types(filepath):
    ingredient_types = {}

    with _open_csv(filepath) as file:
        reader = csv.DictReader(file)

        # Check required columns
        _validate_columns(reader, filepath, {"ingredient", "type"})

        # Read each row
        for row_number, row in enumerate(reader, start=2):
            ingredient = (row.get("ingredient") or "").strip()
            ingredient_type = (row.get("type") or "").strip()

            # Check empty values
            if not ingredient:
                raise DataValidationError(
                    f"{filepath}, row {row_number}: ingredient cannot be empty"
                )

            if not ingredient_type:
                raise DataValidationError(
                    f"{filepath}, row {row_number}: type cannot be empty "
                    f"for ingredient {ingredient!r}"
                )

            # Check duplicate ingredients
            if ingredient in ingredient_types:
                raise DataValidationError(
                    f"{filepath}, row {row_number}: duplicate ingredient "
                    f"{ingredient!r}"
                )

            # Store to ingredient_types
            ingredient_types[ingredient] = ingredient_type

    return ingredient_types


def load_crafting_recipes(filepath):
    recipes = {}

    with _open_csv(filepath) as file:
        reader = csv.DictReader(file)

        # Check required column
        _validate_columns(reader, filepath, {"product", "ingredients"})

        # Read each row
        for row_number, row in enumerate(reader, start=2):
            product = (row.get("product") or "").strip()
            ingredients_text = (row.get("ingredients") or "").strip()

            # Check empty values
            if not product:
                raise DataValidationError(
                    f"{filepath}, row {row_number}: product cannot be empty"
                )

            if not ingredients_text:
                raise DataValidationError(
                    f"{filepath}, row {row_number}: ingredients cannot be empty "
                    f"for product {product!r}"
                )

            # Check duplicate products
            if product in recipes:
                raise DataValidationError(
                    f"{filepath}, row {row_number}: duplicate crafting recipe "
                    f"for product {product!r}"
                )

            # Split ingredients using +
            ingredients = [
                ingredient.strip() for ingredient in ingredients_text.split("+")
            ]

            # Check for empty ingredient tokens
            if any(not ingredient for ingredient in ingredients):
                raise DataValidationError(
                    f"{filepath}, row {row_number}: invalid ingredient list "
                    f"for product {product!r}"
                )

            # Create Recipe object
            recipe = rc.Recipe(product, ingredients)

            # Store to recipes
            recipes[product] = recipe

    return recipes


def load_menus(filepath):
    menus = {}

    with _open_csv(filepath) as file:
        reader = csv.DictReader(file)

        # Check required column
        _validate_columns(
            reader, filepath, {"menu", "level", "sellprice", "equipment", "ingredients"}
        )

        # Read each row
        for row_number, row in enumerate(reader, start=2):
            menu_name = (row.get("menu") or "").strip()
            level_text = (row.get("level") or "").strip()
            price_text = (row.get("sellprice") or "").strip()
            rp_text = (row.get("rp") or "").strip()
            equip_text = (row.get("equipment") or "").strip()
            ingredients_text = (row.get("ingredients") or "").strip()

            # Check empty values
            if not menu_name:
                raise DataValidationError(
                    f"{filepath}, row {row_number}: menu name cannot be empty"
                )

            # Check duplicate menus
            if menu_name in menus:
                raise DataValidationError(
                    f"{filepath}, row {row_number}: duplicate menu {menu_name!r}"
                )

            for field, value in (
                ("level", level_text),
                ("sellprice", price_text),
                ("rp", rp_text),
                ("equipment", equip_text),
                ("ingredients", ingredients_text),
            ):
                if not value:
                    raise DataValidationError(
                        f"{filepath}, row {row_number}: {field} cannot be empty "
                        f"for menu {menu_name}"
                    )

            # Convert to integer for level and sellprice
            try:
                cooking_level = int(level_text)
            except ValueError as exc:
                raise DataValidationError(
                    f"{filepath}, row {row_number}: invalid level "
                    f"{level_text!r} for menu {menu_name!r}; expected an integer"
                ) from exc

            try:
                sell_price = int(price_text)
            except ValueError as exc:
                raise DataValidationError(
                    f"{filepath}, row {row_number}: invalid sellprice "
                    f"{price_text!r} for menu {menu_name!r}; expected an integer"
                ) from exc

            try:
                rp = int(rp_text)
            except ValueError as exc:
                raise DataValidationError(
                    f"{filepath}, row {row_number}: invalid RP "
                    f"{rp_text!r} for menu {menu_name!r}; expected an integer"
                ) from exc

            # Check negative value for level and sellprice
            for field, value in (
                ("level", cooking_level),
                ("sellprice", sell_price),
                ("rp", rp),
            ):
                if value < 0:
                    raise DataValidationError(
                        f"{filepath}, row {row_number}: {field} cannot be negative "
                        f"for menu {menu_name!r}"
                    )

            # Split ingredient using +
            ingredients = [
                ingredient.strip() for ingredient in ingredients_text.split("+")
            ]

            # Check for empty ingredient tokens
            if any(not ingredient for ingredient in ingredients):
                raise DataValidationError(
                    f"{filepath}, row {row_number}: invalid ingredient list "
                    f"for menu {menu_name!r}"
                )

            # Create Recipe object
            recipe = rc.Recipe(menu_name, ingredients)

            # Create Menu object
            menu = Menu(
                name=menu_name,
                recipe=recipe,
                sell_price=sell_price,
                cooking_level=cooking_level,
                rp=rp,
                equipment=equip_text,
            )

            # Store to menus
            menus[menu_name] = menu

    return menus


def load_config(filepath):
    config = {}

    with _open_csv(filepath) as file:
        reader = csv.DictReader(file)

        _validate_columns(
            reader,
            filepath,
            {"setting", "value"},
        )

        for row_number, row in enumerate(reader, start=2):
            setting = (row.get("setting") or "").strip()
            value = (row.get("value") or "").strip()

            if not setting:
                raise DataValidationError(
                    f"{filepath}, row {row_number}: setting cannot be empty"
                )

            if not value:
                raise DataValidationError(
                    f"{filepath}, row {row_number}: value cannot be empty "
                    f"for setting {setting!r}"
                )

            if setting in config:
                raise DataValidationError(
                    f"{filepath}, row {row_number}: duplicate configuration "
                    f"setting {setting!r}"
                )

            config[setting] = value

    return config


def validate_config(config):
    """Validate required application settings and their numeric values."""
    required_settings = {
        "player_cooking_level": 0,
        "target_dish_count": 1,
    }

    validated_config = {}

    for setting, minimum in required_settings.items():
        if setting not in config:
            raise ConfigurationError(
                f"Missing required configuration setting: {setting}"
            )

        value_text = config[setting]

        try:
            value = int(value_text)
        except ValueError as exc:
            raise ConfigurationError(
                f"Invalid configuration value for {setting}: "
                f"{value_text!r}; expected an integer"
            ) from exc

        if value < minimum:
            raise ConfigurationError(
                f"Invalid configuration value for {setting}: {value}; "
                f"minimum allowed value is {minimum}"
            )

        validated_config[setting] = value

    return validated_config


def build_type_members(ingredient_types):
    type_members = {}

    for ingredient, ingredient_type in ingredient_types.items():
        if ingredient_type not in type_members:
            type_members[ingredient_type] = []

        type_members[ingredient_type].append(ingredient)

    return type_members
