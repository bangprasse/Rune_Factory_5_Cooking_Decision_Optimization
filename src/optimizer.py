import pulp


class BasicOptimizer:
    """
    Maximizing revenue for an exact number of dishes
    respecting inventory and crafting raw-material constraint consumption
    """

    def __init__(
        self,
        menu_prices,
        target_dishes,
        menu_ingredients,
        inventory,
        crafting_recipes=None,
    ):
        self.menu_prices = menu_prices
        self.target_dishes = target_dishes
        self.menu_ingredients = menu_ingredients
        self.inventory = inventory
        self.crafting_recipes = crafting_recipes or {}

    def solve(self):
        # 1. Create the optimization problem
        problem = pulp.LpProblem("Rune_Factory_5_Cooking_Optimizer", pulp.LpMaximize)

        # 2. Menu cooking variables
        quantities = {
            menu: problem.add_variable(f"x_{menu}", lowBound=0, cat=pulp.LpInteger)
            for menu in self.menu_prices
        }

        # 3. Crafting variables
        crafted = {
            product: problem.add_variable(
                f"c_{product}", lowBound=0, cat=pulp.LpInteger
            )
            for product in self.crafting_recipes
        }

        # 4. Define the objective: maximize total revenue
        problem += pulp.lpSum(
            self.menu_prices[menu] * quantities[menu] for menu in self.menu_prices
        )

        # 5. Require exactly the target number of dishes
        problem += pulp.lpSum(quantities.values()) == self.target_dishes

        # 6. Collect every ingredient involved in the model
        all_ingredient = set(self.inventory)

        for menu_requirements in self.menu_ingredients.values():
            all_ingredient.update(menu_requirements)

        for product, recipe in self.crafting_recipes.items():
            all_ingredient.add(product)
            all_ingredient.update(recipe)

        # 7. Inventory constraints
        for ingredient in all_ingredient:

            # Ingredient consumed by cooking
            menu_consumption = pulp.lpSum(
                self.menu_ingredients.get(menu, {}).get(ingredient, 0)
                * quantities[menu]
                for menu in self.menu_prices
            )

            # Ingredient consumed by crafting
            crafting_consumption = pulp.lpSum(
                self.crafting_recipes[product].get(ingredient, 0) * crafted[product]
                for product in self.crafting_recipes
            )

            # Ingredient produced by crafting
            crafted_output = crafted.get(ingredient, 0)

            # Total consumption cannot exceed available quantity
            problem += (
                menu_consumption + crafting_consumption
                <= self.inventory.get(ingredient, 0) + crafted_output
            )

        # 8. Solve using CBC
        stats = problem.solve(pulp.COIN_CMD(msg=False))
        status = stats.status_str

        # 8.1 Handle cases where infeasible or unsusccesfull solutions
        if not stats.has_solution:
            return {
                "status": status,
                "menu_quantities": {},
                "crafted_quantities": {},
                "total_dishes": 0,
                "total_revenue": None,
                "ingredient_consumption": {},
                "remaining_inventory": {},
            }

        # 9. Extract selected menus
        selected_menus = {
            menu: int(round(pulp.value(variable)))
            for menu, variable in quantities.items()
            if pulp.value(variable) > 0
        }

        # 10. Extract selected crafting quantities
        crafted_quantities = {
            product: int(round(pulp.value(variable)))
            for product, variable in crafted.items()
            if pulp.value(variable) > 0
        }

        # 11. Calculate menu ingredient consumption
        ingredient_consumption = {}

        for menu, quantity in selected_menus.items():
            for ingredient, amount in self.menu_ingredients.get(menu, {}).items():
                ingredient_consumption[ingredient] = (
                    ingredient_consumption.get(ingredient, 0) + amount * quantity
                )

        # 12. Calculate crafting ingredient consumption
        for product, quantity in crafted_quantities.items():
            for ingredient, amount in self.crafting_recipes[product].items():
                ingredient_consumption[ingredient] = (
                    ingredient_consumption.get(ingredient, 0) + amount * quantity
                )

        # 13. Calculate remaining inventory
        remaining_inventory = {}

        for ingredient in all_ingredient:
            available = self.inventory.get(ingredient, 0)
            produced = crafted_quantities.get(ingredient, 0)
            consumed = ingredient_consumption.get(ingredient, 0)

            remaining_inventory[ingredient] = available + produced - consumed

        # 14. Return the optimization result
        return {
            "status": status,
            "menu_quantities": selected_menus,
            "crafted_quantities": crafted_quantities,
            "total_dishes": sum(selected_menus.values()),
            "total_revenue": int(round(stats.objective)),
            "ingredient_consumption": ingredient_consumption,
            "remaining_inventory": remaining_inventory,
        }
