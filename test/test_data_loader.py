import pytest

from src.data_loader import (
    load_inventory,
    load_ingredient_types,
    load_crafting_recipes,
    load_menus,
    load_config,
    validate_config,
)
from src.exceptions import DataValidationError, ConfigurationError


def write_csv(tmp_path, content):
    filepath = tmp_path / "inventory.csv"
    filepath.write_text(content, encoding="utf-8")
    return filepath


def test_load_inventory_valid_data(tmp_path):
    filepath = write_csv(
        tmp_path,
        "ingredient,quantity\nrice,5\nturnip,3\n",
    )

    assert load_inventory(filepath) == {
        "rice": 5,
        "turnip": 3,
    }


def test_load_inventory_allows_zero_quantity(tmp_path):
    filepath = write_csv(
        tmp_path,
        "ingredient,quantity\nrice,0\n",
    )

    assert load_inventory(filepath) == {"rice": 0}


def test_load_inventory_missing_column(tmp_path):
    filepath = write_csv(tmp_path, "ingredient\nrice\n")

    with pytest.raises(DataValidationError, match="quantity"):
        load_inventory(filepath)


def test_load_inventory_empty_ingredient(tmp_path):
    filepath = write_csv(
        tmp_path,
        "ingredient,quantity\n,5\n",
    )

    with pytest.raises(DataValidationError, match="ingredient"):
        load_inventory(filepath)


def test_load_inventory_invalid_quantity(tmp_path):
    filepath = write_csv(
        tmp_path,
        "ingredient,quantity\nrice,abc\n",
    )

    with pytest.raises(DataValidationError, match="expected an integer"):
        load_inventory(filepath)


def test_load_inventory_negative_quantity(tmp_path):
    filepath = write_csv(
        tmp_path,
        "ingredient,quantity\nrice,-1\n",
    )

    with pytest.raises(DataValidationError, match="negative"):
        load_inventory(filepath)


def test_load_inventory_duplicate_ingredient(tmp_path):
    filepath = write_csv(
        tmp_path,
        "ingredient,quantity\nrice,5\nrice,3\n",
    )

    with pytest.raises(DataValidationError, match="duplicate"):
        load_inventory(filepath)


def test_load_inventory_missing_file(tmp_path):
    filepath = tmp_path / "missing.csv"

    with pytest.raises(DataValidationError, match="Cannot open CSV"):
        load_inventory(filepath)


def test_load_ingredient_types_valid_data(tmp_path):
    filepath = tmp_path / "ingredient_types.csv"
    filepath.write_text(
        "ingredient,type\nTurnip,Vegetable\nPotato,Vegetable\n",
        encoding="utf-8",
    )

    assert load_ingredient_types(filepath) == {
        "Turnip": "Vegetable",
        "Potato": "Vegetable",
    }


def test_load_ingredient_types_missing_column(tmp_path):
    filepath = tmp_path / "ingredient_types.csv"
    filepath.write_text("ingredient\nTurnip\n", encoding="utf-8")

    with pytest.raises(DataValidationError, match="type"):
        load_ingredient_types(filepath)


def test_load_ingredient_types_empty_ingredient(tmp_path):
    filepath = tmp_path / "ingredient_types.csv"
    filepath.write_text("ingredient,type\n,Vegetable\n", encoding="utf-8")

    with pytest.raises(DataValidationError, match="ingredient"):
        load_ingredient_types(filepath)


def test_load_ingredient_types_empty_type(tmp_path):
    filepath = tmp_path / "ingredient_types.csv"
    filepath.write_text("ingredient,type\nTurnip,\n", encoding="utf-8")

    with pytest.raises(DataValidationError, match="type cannot be empty"):
        load_ingredient_types(filepath)


def test_load_ingredient_types_duplicate_ingredient(tmp_path):
    filepath = tmp_path / "ingredient_types.csv"
    filepath.write_text(
        "ingredient,type\nTurnip,Vegetable\nTurnip,Root\n",
        encoding="utf-8",
    )

    with pytest.raises(DataValidationError, match="duplicate"):
        load_ingredient_types(filepath)


def test_load_ingredient_types_missing_file(tmp_path):
    filepath = tmp_path / "missing.csv"

    with pytest.raises(DataValidationError, match="Cannot open CSV"):
        load_ingredient_types(filepath)


def test_load_crafting_recipes_valid_data(tmp_path):
    filepath = tmp_path / "crafting_recipes.csv"
    filepath.write_text(
        "product,ingredients\n" "Pickled Turnip,Turnip\n" "Mixed Juice,Apple + Grape\n",
        encoding="utf-8",
    )

    recipes = load_crafting_recipes(filepath)

    assert recipes["Pickled Turnip"].ingredients == ["Turnip"]
    assert recipes["Mixed Juice"].ingredients == ["Apple", "Grape"]


def test_load_crafting_recipes_trims_ingredients(tmp_path):
    filepath = tmp_path / "crafting_recipes.csv"
    filepath.write_text(
        "product,ingredients\n" "Mixed Juice, Apple +  Grape \n",
        encoding="utf-8",
    )

    recipes = load_crafting_recipes(filepath)

    assert recipes["Mixed Juice"].ingredients == ["Apple", "Grape"]


def test_load_crafting_recipes_missing_column(tmp_path):
    filepath = tmp_path / "crafting_recipes.csv"
    filepath.write_text("product\nPickled Turnip\n", encoding="utf-8")

    with pytest.raises(DataValidationError, match="ingredients"):
        load_crafting_recipes(filepath)


def test_load_crafting_recipes_empty_product(tmp_path):
    filepath = tmp_path / "crafting_recipes.csv"
    filepath.write_text("product,ingredients\n,Turnip\n", encoding="utf-8")

    with pytest.raises(DataValidationError, match="product cannot be empty"):
        load_crafting_recipes(filepath)


def test_load_crafting_recipes_empty_ingredients(tmp_path):
    filepath = tmp_path / "crafting_recipes.csv"
    filepath.write_text("product,ingredients\nPickled Turnip,\n", encoding="utf-8")

    with pytest.raises(DataValidationError, match="ingredients cannot be empty"):
        load_crafting_recipes(filepath)


@pytest.mark.parametrize(
    "ingredients",
    ["Turnip +", "+Turnip", "Turnip ++ Potato"],
)
def test_load_crafting_recipes_invalid_ingredient_list(tmp_path, ingredients):
    filepath = tmp_path / "crafting_recipes.csv"
    filepath.write_text(
        f"product,ingredients\nPickled Turnip,{ingredients}\n",
        encoding="utf-8",
    )

    with pytest.raises(DataValidationError, match="invalid ingredient list"):
        load_crafting_recipes(filepath)


def test_load_crafting_recipes_duplicate_product(tmp_path):
    filepath = tmp_path / "crafting_recipes.csv"
    filepath.write_text(
        "product,ingredients\n"
        "Pickled Turnip,Turnip\n"
        "Pickled Turnip,Turnip + Salt\n",
        encoding="utf-8",
    )

    with pytest.raises(DataValidationError, match="duplicate crafting recipe"):
        load_crafting_recipes(filepath)


def test_load_crafting_recipes_missing_file(tmp_path):
    filepath = tmp_path / "missing.csv"

    with pytest.raises(DataValidationError, match="Cannot open CSV"):
        load_crafting_recipes(filepath)


def write_menu_csv(tmp_path, content):
    filepath = tmp_path / "menus.csv"
    filepath.write_text(content, encoding="utf-8")
    return filepath


def test_load_menus_valid_data(tmp_path):
    filepath = write_menu_csv(
        tmp_path,
        "menu,level,sellprice,rp,equipment,ingredients,effects\n"
        "onigiri,2,57,0,cooking_table,rice,HP Recovery\n"
        "pickles,10,105,5,cooking_table,cucumber,HP Recovery\n",
    )

    menus = load_menus(filepath)

    assert menus["onigiri"].name == "onigiri"
    assert menus["onigiri"].cooking_level == 2
    assert menus["onigiri"].sell_price == 57
    assert menus["onigiri"].rp == 0
    assert menus["onigiri"].equipment == "cooking_table"
    assert menus["onigiri"].recipe.ingredients == ["rice"]

    assert menus["pickles"].rp == 5


def test_load_menus_missing_rp_column(tmp_path):
    filepath = write_menu_csv(
        tmp_path,
        "menu,level,sellprice,equipment,ingredients\n"
        "onigiri,2,57,cooking_table,rice\n",
    )

    with pytest.raises(DataValidationError, match="rp"):
        load_menus(filepath)


@pytest.mark.parametrize(
    "field,value,error",
    [
        ("level", "abc", "invalid level"),
        ("sellprice", "abc", "invalid sellprice"),
        ("rp", "abc", "invalid RP"),
    ],
)
def test_load_menus_invalid_numeric_values(tmp_path, field, value, error):
    columns = ["menu", "level", "sellprice", "rp", "equipment", "ingredients"]
    values = ["onigiri", "2", "57", "0", "cooking_table", "rice"]
    values[columns.index(field)] = value

    filepath = write_menu_csv(
        tmp_path,
        ",".join(columns) + "\n" + ",".join(values) + "\n",
    )

    with pytest.raises(DataValidationError, match=error):
        load_menus(filepath)


@pytest.mark.parametrize("field", ["level", "sellprice", "rp"])
def test_load_menus_negative_numeric_values(tmp_path, field):
    columns = ["menu", "level", "sellprice", "rp", "equipment", "ingredients"]
    values = ["onigiri", "2", "57", "0", "cooking_table", "rice"]
    values[columns.index(field)] = "-1"

    filepath = write_menu_csv(
        tmp_path,
        ",".join(columns) + "\n" + ",".join(values) + "\n",
    )

    with pytest.raises(DataValidationError, match="cannot be negative"):
        load_menus(filepath)


def test_load_menus_empty_rp(tmp_path):
    filepath = write_menu_csv(
        tmp_path,
        "menu,level,sellprice,rp,equipment,ingredients\n"
        "onigiri,2,57,,cooking_table,rice\n",
    )

    with pytest.raises(DataValidationError, match="rp cannot be empty"):
        load_menus(filepath)


def test_load_menus_duplicate_menu(tmp_path):
    filepath = write_menu_csv(
        tmp_path,
        "menu,level,sellprice,rp,equipment,ingredients\n"
        "onigiri,2,57,0,cooking_table,rice\n"
        "onigiri,3,60,0,cooking_table,rice\n",
    )

    with pytest.raises(DataValidationError, match="duplicate menu"):
        load_menus(filepath)


@pytest.mark.parametrize(
    "ingredients",
    ["rice +", "+rice", "rice ++ turnip"],
)
def test_load_menus_invalid_ingredients(tmp_path, ingredients):
    filepath = write_menu_csv(
        tmp_path,
        "menu,level,sellprice,rp,equipment,ingredients\n"
        f"onigiri,2,57,0,cooking_table,{ingredients}\n",
    )

    with pytest.raises(DataValidationError, match="invalid ingredient list"):
        load_menus(filepath)


def test_load_menus_missing_file(tmp_path):
    filepath = tmp_path / "missing.csv"

    with pytest.raises(DataValidationError, match="Cannot open CSV"):
        load_menus(filepath)


def test_load_config_valid_data(tmp_path):
    filepath = tmp_path / "config.csv"
    filepath.write_text(
        "setting,value\n" "player_cooking_level,55\n" "target_dish_count,10\n",
        encoding="utf-8",
    )

    assert load_config(filepath) == {
        "player_cooking_level": "55",
        "target_dish_count": "10",
    }


def test_load_config_missing_column(tmp_path):
    filepath = tmp_path / "config.csv"
    filepath.write_text("setting\nplayer_cooking_level\n", encoding="utf-8")

    with pytest.raises(DataValidationError, match="value"):
        load_config(filepath)


def test_load_config_empty_setting(tmp_path):
    filepath = tmp_path / "config.csv"
    filepath.write_text("setting,value\n,55\n", encoding="utf-8")

    with pytest.raises(DataValidationError, match="setting cannot be empty"):
        load_config(filepath)


def test_load_config_empty_value(tmp_path):
    filepath = tmp_path / "config.csv"
    filepath.write_text(
        "setting,value\nplayer_cooking_level,\n",
        encoding="utf-8",
    )

    with pytest.raises(DataValidationError, match="value cannot be empty"):
        load_config(filepath)


def test_load_config_duplicate_setting(tmp_path):
    filepath = tmp_path / "config.csv"
    filepath.write_text(
        "setting,value\n" "player_cooking_level,55\n" "player_cooking_level,60\n",
        encoding="utf-8",
    )

    with pytest.raises(DataValidationError, match="duplicate"):
        load_config(filepath)


def test_load_config_missing_file(tmp_path):
    filepath = tmp_path / "missing.csv"

    with pytest.raises(DataValidationError, match="Cannot open CSV"):
        load_config(filepath)


def test_validate_config_valid_values():
    config = {
        "player_cooking_level": "55",
        "target_dish_count": "10",
    }

    assert validate_config(config) == {
        "player_cooking_level": 55,
        "target_dish_count": 10,
    }


def test_validate_config_allows_zero_cooking_level():
    config = {
        "player_cooking_level": "0",
        "target_dish_count": "1",
    }

    assert validate_config(config)["player_cooking_level"] == 0


def test_validate_config_rejects_zero_target():
    config = {
        "player_cooking_level": "55",
        "target_dish_count": "0",
    }

    with pytest.raises(ConfigurationError, match="minimum allowed value is 1"):
        validate_config(config)


@pytest.mark.parametrize(
    "setting",
    ["player_cooking_level", "target_dish_count"],
)
def test_validate_config_rejects_missing_setting(setting):
    config = {
        "player_cooking_level": "55",
        "target_dish_count": "10",
    }
    del config[setting]

    with pytest.raises(ConfigurationError, match=setting):
        validate_config(config)


@pytest.mark.parametrize(
    "setting",
    ["player_cooking_level", "target_dish_count"],
)
def test_validate_config_rejects_non_integer(setting):
    config = {
        "player_cooking_level": "55",
        "target_dish_count": "10",
    }
    config[setting] = "abc"

    with pytest.raises(ConfigurationError, match="expected an integer"):
        validate_config(config)


def test_validate_config_rejects_negative_cooking_level():
    config = {
        "player_cooking_level": "-1",
        "target_dish_count": "10",
    }

    with pytest.raises(ConfigurationError, match="minimum allowed value is 0"):
        validate_config(config)


def test_validate_config_rejects_negative_target():
    config = {
        "player_cooking_level": "55",
        "target_dish_count": "-1",
    }

    with pytest.raises(ConfigurationError, match="minimum allowed value is 1"):
        validate_config(config)
