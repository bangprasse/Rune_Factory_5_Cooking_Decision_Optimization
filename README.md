# Rune_Factory_5_Cooking_Decision_Optimization
It is python mini project that calculate best decision for cooking in Rune Factory 5 base on ingredient we have.


<!-- Project Structure -->
Rune_Factory_5_Cooking_Decision_Optimization/
│                       
├── data/                           # editable game data, separate from source code
│   ├── inventory.csv               # ingredient names and available quantities; can include raw and crafted ingredients
│   ├── crafting_recipes.csv        # product and required ingredients
│   ├── ingredient_types.csv        # concrete ingredient members and their app-defined substitution type
│   ├── menus.csv                   # menu name, final selling price, required cooking level, 
|   |                                 RP, equipment, ingredients,   and effects
│   └── config.csv                  # player cooking level and configurable settings
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── ingredient.py
│   ├── recipe.py
│   ├── menu.py
│   ├── data_loader.py
│   ├── recipe_resolver.py
│   ├── optimizer.py
│   └── result.py
│
├── tests/
│   └── test_recipes.py
│
├── requirements.txt
├── README.md                       # Project documentation and usage instructions
└── PROJECT_GUIDE.md

<!-- Workflow -->
