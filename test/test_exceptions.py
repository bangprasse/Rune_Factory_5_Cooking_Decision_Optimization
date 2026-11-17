import pytest

from src.exceptions import (
    GameOptimizerError,
    DataValidationError,
    ConfigurationError,
    RecipeResolutionError,
    OptimizationError,
)


@pytest.mark.parametrize(
    "error_class",
    [
        DataValidationError,
        ConfigurationError,
        RecipeResolutionError,
        OptimizationError,
    ],
)
def test_specialized_errors_inherit_from_base(error_class):
    error = error_class("test error")

    assert isinstance(error, GameOptimizerError)
    assert str(error) == "test error"


def test_base_error_can_be_raised():
    with pytest.raises(GameOptimizerError):
        raise GameOptimizerError("application error")
