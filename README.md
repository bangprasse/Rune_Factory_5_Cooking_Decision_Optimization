# Rune_Factory_5_Cooking_Decision_Optimization
It is python mini project that calculate best decision for cooking in Rune Factory 5 base on ingredient we have.


<!-- Project Structure -->
Rune_Factory_5_Cooking_Decision_Optimization/
│
├── data/                             # Stores game data in CSV format
│   │
│   ├── inventory.csv                 # Available ingredients and their quantities
│   ├── crafting_recipes.csv          # Crafting recipes and their ingredients
│   ├── menus.csv                     # Menus, prices, levels, RP, and ingredients
│   └── config.csv                    # Player settings and optimization configuration
│
├── notebooks/                        # Contains Python notebooks (.ipynb)
│   │
│   ├── 01_classes.ipynb              # Defines Ingredient, Recipe, and Menu classes
│   ├── 02_data_loader.ipynb          # Loads CSV data and creates Python objects
│   ├── 03_recipe_resolver.ipynb      # Expands crafting ingredients recursively
│   ├── 04_optimizer.ipynb            # Optimizes menu combinations using ILP
│   └── 05_main.ipynb                 # Executes the complete optimization workflow
│
└── README.md                         # Project documentation and usage instructions


<!-- Workflow -->
