from ingredient import Ingredient
from recipe import Recipe
from menu import Menu

fried_rice = Recipe("fried_rice", {"rice": 1, "oil": 1, "egg_(s-l)": 1})

omuraisu = Menu(
    'Omuraisu',
    fried_rice,
    12000,
    41
)

print(omuraisu)
