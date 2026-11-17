from types import SimpleNamespace

import pytest

from src import main as main_module
from src.exceptions import DataValidationError


def test_main_stops_when_dataset_is_invalid(monkeypatch):
    # Provide a valid configuration
    settings = {
        "player_cooking_level": 10,
        "target_dish_count": 1,
    }

    monkeypatch.setattr(
        main_module.dl,
        "load_config",
        lambda _: settings,
    )

    monkeypatch.setattr(
        main_module.dl,
        "validate_config",
        lambda settings: settings,
    )

    # Provide empty inventory, recipes, and ingredient types
    monkeypatch.setattr(
        main_module.dl,
        "load_inventory",
        lambda _: {},
    )

    monkeypatch.setattr(
        main_module.dl,
        "load_ingredient_types",
        lambda _: {},
    )

    monkeypatch.setattr(
        main_module.dl,
        "load_crafting_recipes",
        lambda _: {},
    )

    # Create a menu with an unknown ingredient
    invalid_menu = SimpleNamespace(
        cooking_level=1,
        sell_price=100,
        rp=0,
        equipment="knife",
        recipe=SimpleNamespace(ingredients=["missing_ingredient"]),
    )

    monkeypatch.setattr(
        main_module.dl,
        "load_menus",
        lambda _: {"test_dish": invalid_menu},
    )

    # The optimizer must never run
    def optimizer_should_not_run(*args, **kwargs):
        pytest.fail("Optimizer ran despite invalid dataset")

    monkeypatch.setattr(
        main_module,
        "BasicOptimizer",
        optimizer_should_not_run,
    )

    # Expect startup validation to stop the application
    with pytest.raises(
        DataValidationError,
        match="missing_ingredient",
    ):
        main_module.main()


def test_run_application_displays_validation_error(monkeypatch, capsys):
    def fail_main():
        raise DataValidationError("Dataset validation failed: missing_ingredient")

    monkeypatch.setattr(main_module, "main", fail_main)

    main_module.run_application()

    captured = capsys.readouterr()

    assert "ERROR:" in captured.out
    assert "missing_ingredient" in captured.out
    assert captured.err == ""
