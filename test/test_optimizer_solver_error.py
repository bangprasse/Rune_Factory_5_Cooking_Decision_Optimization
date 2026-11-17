import pytest
import pulp

from src.optimizer import BasicOptimizer
from src.exceptions import OptimizationError


def make_optimizer():
    return BasicOptimizer(
        menu_prices={"Soup": 100},
        target_dishes=2,
        menu_ingredients={"Soup": {"Rice": 1}},
        inventory={"Rice": 5},
    )


def test_solver_exception_is_wrapped(monkeypatch):
    optimizer = make_optimizer()
    problem = pulp.LpProblem("test")

    def failing_solve(*args, **kwargs):
        raise RuntimeError("solver crashed")

    monkeypatch.setattr(
        pulp.LpProblem,
        "solve",
        failing_solve,
    )

    with pytest.raises(
        OptimizationError,
        match="revenue maximization",
    ) as exc_info:
        optimizer._solve_problem(
            problem,
            "revenue maximization",
        )

    assert isinstance(exc_info.value.__cause__, RuntimeError)
    assert "solver crashed" in str(exc_info.value)
