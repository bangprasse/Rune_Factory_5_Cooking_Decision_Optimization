from optimizer import BasicOptimizer

menu_prices = {"test_dish": 100}

# One dish requires:
# 1 lamp_squid specifically
# 1 additional squid of any type
menu_ingredients = {"test_dish": {"lamp_squid": 1, "type:squid": 1}}

inventory = {"lamp_squid": 1, "squid": 0, "sunsquid": 0}

type_members = {"squid": ["lamp_squid", "squid", "sunsquid"]}

optimizer = BasicOptimizer(
    menu_prices=menu_prices,
    target_dishes=1,
    menu_ingredients=menu_ingredients,
    inventory=inventory,
    type_members=type_members,
)

result = optimizer.solve()

print("\nSpecific + Type Test")
print(result)

assert result["status"] == "Optimal"
assert result["total_dishes"] == 1

# Specific lamp_squid + type allocation squid
assert result["ingredient_consumption"]["lamp_squid"] == 1
assert result["ingredient_consumption"]["squid"] == 1

assert result["remaining_inventory"]["lamp_squid"] == 0
assert result["remaining_inventory"]["squid"] == 0

print("\nSpecific + type allocation test passed!")
