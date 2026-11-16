from src.result import OptimizationResult


def create_result(status):
    return OptimizationResult(
        status=status,
        player_cooking_level=50,
        target_dish_count=10,
        selected_menus={},
        total_dishes=10 if status == "OPTIMAL" else 0,
        total_revenue=25000 if status == "OPTIMAL" else 0,
        total_rp=120 if status == "OPTIMAL" else 0,
        ingredient_usage={},
        remaining_inventory={},
    )


def test_optimal_result():
    result = create_result("OPTIMAL")

    assert result.is_optimal() is True
    assert result.is_feasible() is True


def test_infeasible_result():
    result = create_result("INFEASIBLE")

    assert result.is_optimal() is False
    assert result.is_feasible() is False


def test_other_solver_status():
    result = create_result("ERROR")

    assert result.is_optimal() is False
    assert result.is_feasible() is False


def test_summary_optimal_result():
    result = create_result("OPTIMAL")

    result.selected_menus = {
        "seafood_doria": {
            "quantity": 3,
            "equipment": "oven",
        },
        "omelet": {
            "quantity": 2,
            "equipment": "frying_pan",
        },
    }

    result.ingredient_usage = {
        "rice": 3,
        "dairy": 6,
    }

    result.remaining_inventory = {
        "rice": 7,
        "dairy": 4,
    }

    report = result.summary()

    assert "Rune Factory 5 Cooking Optimizaiton" in report
    assert "Status: OPTIMAL" in report
    assert "seafood_doria x3 (oven)" in report
    assert "omelet x2 (frying_pan)" in report
    assert "Ingredient Usage:" in report
    assert "Remaining Inventory:" in report


def test_summary_infeasible_result():
    result = create_result("INFEASIBLE")

    report = result.summary()

    assert "No feasible cooking plan was found" in report
    assert "Selected Menus:" not in report
    assert "Total Revenue:" not in report


def test_display(capsys):
    result = create_result("OPTIMAL")

    result.display()

    captured = capsys.readouterr()

    assert "Rune Factory 5 Cooking Optimizaiton" in captured.out
    assert "Status: OPTIMAL" in captured.out
