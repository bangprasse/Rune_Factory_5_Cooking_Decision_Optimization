import pulp


class BasicOptimizer:
    """
    Maximizing revenue for an exact number of dishes,
    respecting inventory, crafting, and type-based ingredient allocation requirements.

    Type allocations are created and linked to menu quantities.
    """

    def __init__(
        self,
        menu_prices,
        target_dishes,
        menu_ingredients,
        inventory,
        crafting_recipes=None,
        type_members=None,
    ):
        self.menu_prices = menu_prices
        self.target_dishes = target_dishes
        self.menu_ingredients = menu_ingredients
        self.inventory = inventory
        self.crafting_recipes = crafting_recipes or {}
        self.type_members = type_members or {}

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

        # 4. Type-based ingredient allocation variables
        type_allocations = {}

        for menu, requirements in self.menu_ingredients.items():
            for ingredient, amount in requirements.items():
                if ingredient.startswith("type:"):
                    ingredient_type = ingredient.replace("type:", "")

                    members = self.type_members.get(ingredient_type, [])

                    for member in members:
                        key = (menu, ingredient_type, member)

                        type_allocations[key] = problem.add_variable(
                            f"a_{menu}_{ingredient_type}_{member}",
                            lowBound=0,
                            cat=pulp.LpInteger,
                        )

        # 5. Define the objective: maximize total revenue
        problem += pulp.lpSum(
            self.menu_prices[menu] * quantities[menu] for menu in self.menu_prices
        )

        # 6. Require exactly the target number of dishes
        problem += pulp.lpSum(quantities.values()) == self.target_dishes

        # 7. Type allocation constraints
        for menu, requirements in self.menu_ingredients.items():
            for ingredient, amount in requirements.items():
                if ingredient.startswith("type:"):
                    ingredient_type = ingredient.replace("type:", "")

                    members = self.type_members.get(ingredient_type, [])

                    problem += (
                        pulp.lpSum(
                            type_allocations[(menu, ingredient_type, member)]
                            for member in members
                        )
                        == amount * quantities[menu]
                    )

        # 8. Collect every ingredient involved in the model
        all_ingredient = set(self.inventory)

        for menu_requirements in self.menu_ingredients.values():
            for ingredient in menu_requirements:
                if not ingredient.startswith("type:"):
                    all_ingredient.add(ingredient)

        for product, recipe in self.crafting_recipes.items():
            all_ingredient.add(product)
            all_ingredient.update(recipe)

        # 9. Inventory constraints
        for ingredient in all_ingredient:

            # Ingredient consumed by cooking
            menu_consumption = pulp.lpSum(
                self.menu_ingredients.get(menu, {}).get(ingredient, 0)
                * quantities[menu]
                for menu in self.menu_prices
            )

            # Consumption through type allocations
            type_consumption = pulp.lpSum(
                variable
                for (
                    menu,
                    ingredient_type,
                    member,
                ), variable in type_allocations.items()
                if member == ingredient
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
                menu_consumption + type_consumption + crafting_consumption
                <= self.inventory.get(ingredient, 0) + crafted_output
            )

        # 10. Stage 1 - Maximize revenue
        stats = problem.solve(pulp.COIN_CMD(msg=False))
        status = stats.status_str

        # Check whether stage 1 found a solution
        if not stats.has_solution:
            return {
                "status": status,
                "menu_quantities": {},
                "crafted_quantities": {},
                "type_allocations": {},
                "total_dishes": 0,
                "total_revenue": None,
                "ingredient_consumption": {},
                "remaining_inventory": {},
            }

        # Save the maximum revenue
        maximum_revenue = int(round(stats.objective))

        # 11. Stage 2 - Preserve revenue and minimize crafting
        problem += (
            pulp.lpSum(
                self.menu_prices[menu] * quantities[menu] for menu in self.menu_prices
            )
            == maximum_revenue
        )

        problem.sense = pulp.LpMinimize

        problem.setObjective(pulp.lpSum(crafted.values()))

        # Solve again
        stats = problem.solve(pulp.COIN_CMD(msg=False))
        status = stats.status_str

        # Check whether stage 1 found a solution
        if not stats.has_solution:
            return {
                "status": status,
                "menu_quantities": {},
                "crafted_quantities": {},
                "type_allocations": {},
                "total_dishes": 0,
                "total_revenue": None,
                "ingredient_consumption": {},
                "remaining_inventory": {},
            }

        # 12. Extract selected menus
        selected_menus = {
            menu: int(round(pulp.value(variable)))
            for menu, variable in quantities.items()
            if pulp.value(variable) > 0
        }

        # 13. Extract selected crafting quantities
        crafted_quantities = {
            product: int(round(pulp.value(variable)))
            for product, variable in crafted.items()
            if pulp.value(variable) > 0
        }

        # 14. Extract type allocations
        selected_type_allocations = {
            key: int(round(pulp.value(variable)))
            for key, variable in type_allocations.items()
            if pulp.value(variable) > 0
        }

        # 15. Calculate menu ingredient consumption
        ingredient_consumption = {}

        for menu, quantity in selected_menus.items():
            for ingredient, amount in self.menu_ingredients.get(menu, {}).items():
                if ingredient.startswith("type:"):
                    continue

                ingredient_consumption[ingredient] = (
                    ingredient_consumption.get(ingredient, 0) + amount * quantity
                )

        # 16. Calculate crafting ingredient consumption
        for product, quantity in crafted_quantities.items():
            for ingredient, amount in self.crafting_recipes[product].items():
                ingredient_consumption[ingredient] = (
                    ingredient_consumption.get(ingredient, 0) + amount * quantity
                )

        # 17. Calculate type allocation consumption
        for (
            menu,
            ingredient_type,
            member,
        ), quantity in selected_type_allocations.items():
            ingredient_consumption[member] = (
                ingredient_consumption.get(member, 0) + quantity
            )

        # 17. Calculate remaining inventory
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
            "type_allocations": selected_type_allocations,
            "total_dishes": sum(selected_menus.values()),
            "total_revenue": maximum_revenue,
            "ingredient_consumption": ingredient_consumption,
            "remaining_inventory": remaining_inventory,
        }
