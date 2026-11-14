import pulp


class BasicOptimizer:
    """
    Maximizing revenue for an exact number of dishes
    No ingredient or crafting constraint yet
    """

    def __init__(self, menu_prices, target_dishes):
        self.menu_prices = menu_prices
        self.target_dishes = target_dishes

    def solve(self):
        # 1. Create the optimization problem
        problem = pulp.LpProblem("Rune_Factory_5_Cooking_Optimizer", pulp.LpMaximize)

        # 2. Create an integer decision variable for each menu
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

        # 5. Solve using CBC
        stats = problem.solve(pulp.COIN_CMD(msg=False))

        # 6. Read the solver status
        status = stats.status_str

        # 7. Handle cases where no solution is available
        if not stats.has_solution:
            return {"status": status, "menu_quantities": {}, "total_revenue": None}

        # 8. Extras menus with positive quantities
        selected_menus = {
            menu: int(round(pulp.value(variable)))
            for menu, variable in quantities.items()
            if pulp.value(variable) > 0
        }

        # 9. Return the optimization result
        return {
            "status": status,
            "menu_quantities": selected_menus,
            "total_revenue": int(round(stats.objective)),
        }
