from src.optimizer import BasicOptimizer


def test_optimizer_maximizes_revenue():
    menu_prices = {
        "Cheap Dish": 100,
        "Expensive Dish": 300,
    }

    menu_ingredients = {
        "Cheap Dish": {"Rice": 1},
        "Expensive Dish": {"Rice": 2},
    }

    inventory = {
        "Rice": 4,
    }

    optimizer = BasicOptimizer(
        menu_prices=menu_prices,
        target_dishes=2,
        menu_ingredients=menu_ingredients,
        inventory=inventory,
    )

    result = optimizer.solve()

    assert result["status"] == "Optimal"
    assert result["total_dishes"] == 2
    assert result["total_revenue"] == 600
    assert result["menu_quantities"] == {
        "Expensive Dish": 2,
    }


def test_optimizer_avoids_unnecessary_crafting():
    menu_prices = {
        "Bread": 200,
    }

    menu_ingredients = {
        "Bread": {"Flour": 1},
    }

    inventory = {
        "Flour": 2,
        "Bread": 2,
    }

    optimizer = BasicOptimizer(
        menu_prices=menu_prices,
        target_dishes=2,
        menu_ingredients=menu_ingredients,
        inventory=inventory,
        crafting_recipes={
            "Bread": {"Flour": 1},
        },
    )

    result = optimizer.solve()

    assert result["status"] == "Optimal"
    assert result["total_dishes"] == 2
    assert result["total_revenue"] == 400
    assert result["crafted_quantities"] == {}


def test_optimizer_crafts_only_missing_quantity():
    menu_prices = {
        "Bread Soup": 200,
    }

    menu_ingredients = {
        "Bread Soup": {"Bread": 1},
    }

    inventory = {
        "Flour": 3,
        "Bread": 1,
    }

    optimizer = BasicOptimizer(
        menu_prices=menu_prices,
        target_dishes=3,
        menu_ingredients=menu_ingredients,
        inventory=inventory,
        crafting_recipes={
            "Bread": {"Flour": 1},
        },
    )

    result = optimizer.solve()

    assert result["status"] == "Optimal"
    assert result["total_dishes"] == 3
    assert result["total_revenue"] == 600
    assert result["crafted_quantities"] == {"Bread": 2}


def test_optimizer_handles_recursive_crafting():
    menu_prices = {"Soup": 300}
    menu_ingredients = {"Soup": {"Soup Base": 1}}
    inventory = {"Flour": 1}

    crafting_recipes = {
        "Bread": {"Flour": 1},
        "Soup Base": {"Bread": 1},
    }

    optimizer = BasicOptimizer(
        menu_prices=menu_prices,
        target_dishes=1,
        menu_ingredients=menu_ingredients,
        inventory=inventory,
        crafting_recipes=crafting_recipes,
    )

    result = optimizer.solve()

    assert result["status"] == "Optimal"
    assert result["total_dishes"] == 1
    assert result["total_revenue"] == 300
    assert result["crafted_quantities"] == {
        "Bread": 1,
        "Soup Base": 1,
    }


def test_optimizer_allocates_type_ingredients():
    menu_prices = {"Vegetable Soup": 250}
    menu_ingredients = {"Vegetable Soup": {"type:vegetable": 2}}
    inventory = {
        "Turnip": 1,
        "Cabbage": 2,
    }
    type_members = {"vegetable": ["Turnip", "Cabbage"]}

    optimizer = BasicOptimizer(
        menu_prices=menu_prices,
        target_dishes=1,
        menu_ingredients=menu_ingredients,
        inventory=inventory,
        type_members=type_members,
    )

    result = optimizer.solve()

    assert result["status"] == "Optimal"
    assert result["total_dishes"] == 1
    assert result["total_revenue"] == 250
    assert sum(result["type_allocations"].values()) == 2
    assert (
        result["ingredient_consumption"]["Turnip"]
        + result["ingredient_consumption"]["Cabbage"]
        == 2
    )


def test_optimizer_handles_specific_and_type_requirements_together():
    menu_prices = {"Vegetable Soup": 300}
    menu_ingredients = {
        "Vegetable Soup": {
            "Turnip": 1,
            "type:vegetable": 1,
        }
    }

    inventory = {
        "Turnip": 1,
        "Cabbage": 1,
    }

    type_members = {
        "vegetable": ["Turnip", "Cabbage"],
    }

    optimizer = BasicOptimizer(
        menu_prices=menu_prices,
        target_dishes=1,
        menu_ingredients=menu_ingredients,
        inventory=inventory,
        type_members=type_members,
    )

    result = optimizer.solve()

    assert result["status"] == "Optimal"
    assert result["total_dishes"] == 1
    assert result["total_revenue"] == 300

    assert result["ingredient_consumption"]["Turnip"] == 1
    assert result["ingredient_consumption"]["Cabbage"] == 1


def test_optimizer_reports_infeasible_target():
    menu_prices = {"Rice Dish": 200}
    menu_ingredients = {"Rice Dish": {"Rice": 1}}
    inventory = {"Rice": 1}

    optimizer = BasicOptimizer(
        menu_prices=menu_prices,
        target_dishes=2,
        menu_ingredients=menu_ingredients,
        inventory=inventory,
    )

    result = optimizer.solve()

    assert result["status"] == "Infeasible"
