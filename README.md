# Rune_Factory_5_Cooking_Decision_Optimization
It is python mini project that calculate best decision for cooking in Rune Factory 5 base on ingredient we have.

## 1. Project Overview

Rune_Factory_5_Cooking_Decision_Optimization is a Python base application for Rune Factory 5 that make a best decision for the most profitable combination of dishes to cook. For the method used is Integer Linear Programming (ILP) to calculate the best decision to cook. 

The current version is a terminal-based application.

For future plan, this project will be upgrade to be a standalone desktop application.

## 2. Features

The current Terminal Edition includes:

- Integer Linear Programming (ILP) optimization using PuLP.
- Exact target dish-count enforcement.
- Maximum total selling revenue.
- Menu eligibility based on the player's cooking level.
- Inventory quantity constraints.
- Support for existing crafted ingredients in inventory.
- Ingredient-type requirements, such as `type:jam`.
- Detection of infeasible optimization problems.
- Reporting of total RP, ingredient usage, and remaining inventory.
- Dataset validation and application-level error handling.

## 3. Project Structure

The project uses the following directory structure:

```text
Rune_Factory_5_Cooking_Decision_Optimzation/
├── data/
│   ├── config.csv
│   ├── inventory.csv
│   ├── crafting_recipes.csv
│   ├── ingredient_types.csv
│   └── menus.csv
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── ingredient.py
│   ├── recipe.py
│   ├── menu.py
│   ├── config.py
│   ├── data_loader.py
│   ├── data_validator.py
│   ├── exceptions.py
│   ├── recipe_resolver.py
│   ├── optimizer.py
│   └── result.py
│
├── tests/
├── requirements.txt
└── README.md
```

### Main modules

- `main.py`: Coordinates the application workflow.
- `config.py`: Defines project data-file paths.
- `data_loader.py`: Loads configuration and game data.
- `data_validator.py`: Checks data integrity.
- `exceptions.py`: Defines application-specific exceptions.
- `ingredient.py`: Represents ingredient data.
- `recipe.py`: Represents crafting recipes.
- `menu.py`: Represents cooking menus.
- `recipe_resolver.py`: Handles recipe dependencies and ingredient requirements.
- `optimizer.py`: Builds and solves the optimization problem.
- `result.py`: Stores and displays optimization results.

## 4. Installation

### Requirements

- Python
- pip
- PuLP

### Install dependencies

Open a terminal in the project root directory and run:

```bash
python -m pip install -r requirements.txt
```

The `requirements.txt` file contains:

```text
pulp
```

## 5. Configuration

The application reads its settings from:

```text
data/config.csv
```

The configuration includes:

| Setting | Description |
|---|---|
| `player_cooking_level` | The player's current cooking level |
| `target_dish_count` | The exact number of dishes to produce |

Edit these values in the CSV file before running the application.

## 6. Dataset Files

All game data is stored separately from the Python source code in the `data/` directory.

| File | Purpose |
|---|---|
| `config.csv` | Player settings and optimization target |
| `inventory.csv` | Available ingredient names and quantities |
| `crafting_recipes.csv` | Crafting products and their ingredients |
| `ingredient_types.csv` | Maps concrete ingredients to application-defined types |
| `menus.csv` | Menu prices, cooking levels, RP, equipment, ingredients, and effects |

### Ingredient requirements

Ingredient lists use `+` as the separator.

For example:

```text
rice+shrimp+squid
```

Specific ingredient requirements use their canonical ingredient names.

Ingredient-type requirements use the reserved format:

```text
type:jam
type:squid
type:mushroom
```

The inventory must contain concrete ingredient names and quantities, not type requirements.

## 7. Running the Application

Make sure to update data inside data/config.csv and data/inventory.csv with actual data from the game.

From the project root directory, run:

```bash
python -m src.main
```

The application will:

1. Load configuration and game data.
2. Validate configuration and relevant dataset information.
3. Filter menus according to the player's cooking level.
4. Resolve ingredient and crafting requirements.
5. Build and solve the optimization problem.
6. Display the optimization result in the terminal.

## 8. Optimization Rules

The optimization objective is:

**Fixed Dish Count → Maximum Total Revenue**

The optimizer must follow these rules:

- Produce exactly the requested number of dishes.
- Maximize total selling revenue.
- Use only menus within the player's cooking level.
- Never exceed available concrete ingredient inventory.
- Use integer, nonnegative menu quantities.
- Account for repeated ingredient requirements.
- Handle recursive crafting dependencies.
- Account for existing crafted inventory without double-counting.
- Allocate type requirements jointly with menu quantities.
- Never consume the same inventory stock twice.

If the exact target dish count cannot be produced, the optimizer must report an infeasible result rather than silently producing fewer dishes.

RP consumption and leftover inventory are reported but are not optimization constraints or objective terms.

## 9. Results

The terminal result includes:

- Solver status.
- Player cooking level.
- Target dish count.
- Selected menus and quantities.
- Total number of dishes.
- Total selling revenue.
- Total RP consumption.
- Concrete ingredient consumption.
- Remaining inventory.
- Crafted quantities.

The initial version returns one optimal combination.

## 10. Error Handling

The application uses custom exceptions to report expected application errors, including:

- Data validation errors.
- Configuration errors.
- Recipe resolution errors.
- Optimization errors.

Expected application errors are displayed as readable terminal messages.

## 11. Testing

Run the project's test suite from the project root:

```bash
python -m pytest -v
```

The tests cover application functionality such as:

- Data loading and validation.
- Recipe resolution.
- Ingredient inventory accounting.
- Ingredient-type requirements.
- Optimization constraints.
- Infeasible optimization cases.
- Application error handling.

If pytest is not installed in your Python environment, install it with:

```bash
python -m pip install pytest
```

## 12. Future Development

Future development may include:

- A standalone desktop interface.
- Alternative optimal menu combinations.
- Additional optimization modes.
- Further reporting and analysis features.

These are future features and are not part of the current Terminal Edition.