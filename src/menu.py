class Menu:
    def __init__(self, name, recipe, sell_price, cooking_level, rp=0, equipment="None"):
        self.name = name
        self.recipe = recipe
        self.sell_price = sell_price
        self.cooking_level = cooking_level
        self.rp = rp
        self.equipment = equipment

    def __repr__(self):
        return (
            f"|Menu| {self.name!r}"
            f"\n|Recipe| {self.recipe!r}"
            f"\n|Sell Price| {self.sell_price!r}G"
            f"\n|Cooking Level| {self.cooking_level}"
            f"\n|Rp| {self.rp}"
            f"\n|Equipment| {self.equipment}"
        )
