import pulp


class BasicOptimizer:
    """
    Maximizing revenue for an exact number of dishes
    while respecting concrete ingredient inventory
    """

    def __init__(self, menu_prices, target_dishes, menu_ingredients, inventory):
        self.menu_prices = menu_prices
        self.target_dishes = target_dishes
        self.menu_ingredients = menu_ingredients
        self.inventory = inventory

    def solve(self):
        # 1. Create the optimization problem
        problem = pulp.LpProblem("Rune_Factory_5_Cooking_Optimizer", pulp.LpMaximize)

        # 2. Create an integer decision variable for each menu quantities
        quantities = {
            menu: problem.add_variable(f"x_{menu}", lowBound=0, cat=pulp.LpInteger)
            for menu in self.menu_prices
        }

        # 3. Definte the objective: maximize total revenue
        problem += pulp.lpSum(
            self.menu_prices[menu] * quantities[menu] for menu in self.menu_prices
        )

        # 4. Require exactly the target number of dishes
        problem += pulp.lpSum(quantities.values()) == self.target_dishes

        # 5. Add concrete ingredient inventory constraints
        for ingredient, available_quantity in self.inventory.items():
            problem += (
                pulp.lpSum(
                    self.menu_ingredients.get(menu, {}).get(ingredient, 0)
                    * quantities[menu]
                    for menu in self.menu_prices
                )
                <= available_quantity
            )

        # 6. Solve using CBC
        stats = problem.solve(pulp.COIN_CMD(msg=False))
        status = stats.status_str

        # 7. Handle cases where infeasible or unsusccesfull solutions
        if not stats.has_solution:
            return {
                "status": status,
                "menu_quantities": {},
                "total_dishes": 0,
                "total_revenue": None,
                "ingredient_consumption": {},
                "remaining_inventory": {},
            }

        # 8. Extras menus with positive quantities
        selected_menus = {
            menu: int(round(pulp.value(variable)))
            for menu, variable in quantities.items()
            if pulp.value(variable) > 0
        }

        # 9. Calculate total ingredient consumption
        ingredient_consumption = {}

        for ingredient in self.inventory:
            consumed = sum(
                self.menu_ingredients.get(menu, {}).get(ingredient, 0) * quantity
                for menu, quantity in selected_menus.items()
            )

            if consumed > 0:
                ingredient_consumption[ingredient] = int(round(consumed))

        # 10. Calculate remainint inventory
        remaining_inventory = {
            ingredient: available_quantity - ingredient_consumption.get(ingredient, 0)
            for ingredient, available_quantity in self.inventory.items()
        }

        # 11. Calculate total dishes
        total_dishes = sum(selected_menus.values())

        # 12. Return the optimization result
        return {
            "status": status,
            "menu_quantities": selected_menus,
            "total_dishes": total_dishes,
            "total_revenue": int(round(stats.objective)),
            "ingredient_consumption": ingredient_consumption,
            "remaining_inventory": remaining_inventory,
        }
