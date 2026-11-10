class Menu:
    def __init__(self, name, recipe, sell_price, cooking_level):
        self.name = name
        self.recipe = recipe
        self.sell_price = sell_price
        self.cooking_level = cooking_level

    def __repr__(self):
        return (
            f"|Menu| {self.name!r}"
            f"\n|Recipe| {self.recipe!r}"
            f"\n|Sell Price| {self.sell_price!r}G"
            f"\n|Cooking Level| {self.cooking_level}"
        )
