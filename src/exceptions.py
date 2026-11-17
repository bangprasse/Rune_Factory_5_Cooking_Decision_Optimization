class GameOptimizerError(Exception):
    """Base exception for application-level errors."""


class DataValidationError(GameOptimizerError):
    """Invalid or inconsistent data in CSV files."""


class ConfigurationError(GameOptimizerError):
    """Invalid or missing application configuration."""


class RecipeResolutionError(GameOptimizerError):
    """Invalid ingredient references or crafting recipe resolution."""


class OptimizationError(GameOptimizerError):
    """Unexpected optimization or solver failure."""
