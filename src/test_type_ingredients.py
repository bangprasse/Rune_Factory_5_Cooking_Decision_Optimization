from optimizer import BasicOptimizer


def test_type_requirement(ingredient_type, members, inventory):
    menu_prices = {"test_dish": 100}

    menu_ingredients = {"test_dish": {f"type:{ingredient_type}": 1}}

    type_members = {ingredient_type: members}

    optimizer = BasicOptimizer(
        menu_prices=menu_prices,
        target_dishes=2,
        menu_ingredients=menu_ingredients,
        inventory=inventory,
        type_members=type_members,
    )

    result = optimizer.solve()

    print(f"\nTesting {ingredient_type}")
    print(result)

    assert result["status"] == "Optimal"
    assert result["total_dishes"] == 2
    assert result["total_revenue"] == 200
    assert sum(result["type_allocations"].values()) == 2
    assert sum(result["ingredient_consumption"].values()) == 2

    print(f"{ingredient_type} test passed!")


# Jam test
test_type_requirement(
    ingredient_type="jam",
    members=["grape_jam", "apple_jam", "strawberry_jam"],
    inventory={"grape_jam": 1, "apple_jam": 1, "strawberry_jam": 2},
)

# Mushroom test
test_type_requirement(
    ingredient_type="mushroom",
    members=["mushroom", "monarch_mushroom"],
    inventory={"mushroom": 1, "monarch_mushroom": 3},
)

print("\nAll jam and mushroom tests passed!")
