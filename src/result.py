class OptimizationResult:
    """Stores the results of a Rune_Factory_5_Cooking_Optimization"""

    def __init__(
        self,
        status,
        player_cooking_level,
        target_dish_count,
        selected_menus,
        total_dishes,
        total_revenue,
        total_rp,
        ingredient_usage,
        remaining_inventory,
    ):
        # Optimization status and input settings
        self.status = status
        self.player_cooking_level = player_cooking_level
        self.target_dish_count = target_dish_count

        # Selected menus, including quantity and equipment
        self.selected_menus = selected_menus

        # Optimization totals
        self.total_dishes = total_dishes
        self.total_revenue = total_revenue
        self.total_rp = total_rp

        # Concrete ingredient accounting
        self.ingredient_usage = ingredient_usage
        self.remaining_inventory = remaining_inventory

    def is_optimal(self):
        return self.status == "OPTIMAL"

    def is_feasible(self):
        return self.status == "OPTIMAL"

    def summary(self):
        """Return a formatted summary of the optimization result"""

        lines = [
            "=" * 45,
            "        Rune Factory 5 Cooking Optimizaiton",
            "=" * 45,
            "",
            f"Status: {self.status}",
            f"Player Cooking Level: {self.player_cooking_level}",
            f"Target Dishes: {self.target_dish_count}",
            "",
        ]

        # Only display cooking details for a feasible solution
        if self.is_feasible():
            lines.append("Selected Menus:")
            lines.append("-" * 45)

            for menu_name, details in self.selected_menus.items():
                quantity = details["quantity"]
                equipment = details["equipment"]

                lines.append(f"{menu_name} x{quantity} ({equipment})")

                lines.append("-" * 45)
                lines.append(f"Total Dishes: {self.total_dishes}")
                lines.append(f"Total Revenue: {self.total_revenue}")
                lines.append(f"Total RP: {self.total_rp:,}")
                lines.append("")

                lines.append("Ingredient Usage:")
                if self.ingredient_usage:
                    for ingredient, quantity in sorted(self.ingredient_usage.items()):
                        lines.append(f"   {ingredient}: {quantity}")
                else:
                    lines.append("   None")
        else:
            lines.append("No feasible cooking plan was found")

        lines.append("")
        lines.append("Remaining Inventory:")

        if self.remaining_inventory:
            for ingredient, quantity in sorted(self.remaining_inventory.items()):
                lines.append(f"  {ingredient}: {quantity}")
        else:
            lines.append("  None")

        lines.append("")
        lines.append("=" * 45)

        return "\n".join(lines)

    def display(self):
        print(self.summary())
