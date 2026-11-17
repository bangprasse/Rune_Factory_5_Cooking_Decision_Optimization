import pytest

from src.optimizer import BasicOptimizer
from src.exceptions import OptimizationError


def make_optimizer(
    target_dishes=2,
    menu_prices=None,
    menu_ingredients=None,
    inventory=None,
):
    return BasicOptimizer(
        menu_prices=menu_prices or {"Soup": 100},
        target_dishes=target_dishes,
        menu_ingredients=menu_ingredients or {"Soup": {"Rice": 1}},
        inventory=inventory or {"Rice": 5},
    )


@pytest.mark.parametrize("target", [0, -1, 1.5, "2", True])
def test_invalid_target_dishes(target):
    with pytest.raises(OptimizationError, match="target_dishes"):
        make_optimizer(target_dishes=target)


def test_valid_target_dishes():
    optimizer = make_optimizer(target_dishes=2)
    assert optimizer.target_dishes == 2


@pytest.mark.parametrize("price", [-1, "100", True])
def test_invalid_menu_price(price):
    with pytest.raises(OptimizationError, match="Invalid price"):
        make_optimizer(menu_prices={"Soup": price})


@pytest.mark.parametrize("quantity", [-1, 1.5, "5", True])
def test_invalid_inventory_quantity(quantity):
    with pytest.raises(OptimizationError, match="Inventory quantity"):
        make_optimizer(inventory={"Rice": quantity})


@pytest.mark.parametrize("amount", [-1, 1.5, "1", True])
def test_invalid_menu_ingredient_amount(amount):
    with pytest.raises(OptimizationError, match="Requirement"):
        make_optimizer(menu_ingredients={"Soup": {"Rice": amount}})


def test_valid_optimizer_inputs():
    optimizer = make_optimizer()
    assert optimizer.target_dishes == 2
