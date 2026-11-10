class Ingredient:
    def __init__(self, name, ingredient_type=None):
        self.name = name
        self.ingredient_type = ingredient_type

    def __repr__(self):
        return f"|Ingredient| '{self.name}'  |Type| '{self.ingredient_type}'"
