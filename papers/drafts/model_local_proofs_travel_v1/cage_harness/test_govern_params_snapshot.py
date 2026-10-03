# Regression test written for the companion paper (public research repository).
# Intended for contribution to the target repository under that repository's own license (Apache-2.0).

"""Regression: the seal must bind the params the stages evaluated.

``SymbolicGovernor.govern()`` passed the caller's live ``params`` dict to the
stages and later to the seal.  A concurrent holder of that dict could change
it after the stages approved it and before the seal was generated, so the
seal bound values no stage had evaluated.  ``govern()`` now snapshots
``params`` on entry; these tests fail if the stages and the seal ever see
different values again.
"""

from __future__ import annotations

import asyncio
import copy
from typing import Any

import pytest

from src.gateway.governance import routing_seal
from src.gateway.governance.governor import sealing
from src.gateway.governance.routing_seal import SymbolicGovernorViolation

pytestmark = [pytest.mark.local, pytest.mark.unit, pytest.mark.regression]


class _EvaluatingStage:
    """Records what it evaluated, then yields so a concurrent task can run."""

    name = "opa"  # runs in the ungoverned profile
    mutating = False

    def __init__(self, on_evaluated=None) -> None:
        self.evaluated: dict[str, Any] | None = None
        self._on_evaluated = on_evaluated

    async def run(self, ctx):  # noqa: ANN001
        self.evaluated = copy.deepcopy(dict(ctx.params))
        if self._on_evaluated is not None:
            self._on_evaluated()
        await asyncio.sleep(0.01)
        return []


@pytest.fixture(autouse=True)
def _hmac_seals(monkeypatch):
    monkeypatch.setenv("CAGE_ENV", "test")
    monkeypatch.setenv("CAGE_SEAL_STRICT_MODE", "false")


def _mutate(params: dict[str, Any]) -> None:
    params["amount"] = 1_000_000.0
    params["meta"]["tags"].append("evil")


def _fresh() -> dict[str, Any]:
    return {"symbol": "AAPL", "amount": 10.0, "meta": {"tags": ["a"]}}


def _plain_fake_issue_seal(monkeypatch, *, before_seal=None):
    async def fake_issue_seal(action: str, params: dict[str, Any], *, path: str) -> str:
        if before_seal is not None:
            before_seal(params)
        await asyncio.sleep(0.01)  # the real issue_seal awaits the evidence commit here
        return routing_seal.generate_seal(action, params, record_hash="rh")

    monkeypatch.setattr(sealing, "issue_seal", fake_issue_seal)


@pytest.mark.parametrize("when", ["after_stage", "during_seal_issuance"])
async def test_seal_binds_params_the_stages_evaluated(governor_factory, monkeypatch, when):
    caller_params = _fresh()
    evaluated_by_stage = copy.deepcopy(caller_params)

    async def mutate_later() -> None:
        await asyncio.sleep(0)
        _mutate(caller_params)

    if when == "after_stage":
        stage = _EvaluatingStage(
            on_evaluated=lambda: asyncio.get_running_loop().create_task(mutate_later())
        )
        _plain_fake_issue_seal(monkeypatch)
    else:
        stage = _EvaluatingStage()
        _plain_fake_issue_seal(
            monkeypatch,
            before_seal=lambda _p: asyncio.get_running_loop().create_task(mutate_later()),
        )

    governor = governor_factory(core_stages=[stage])
    seal = await governor.govern("execute_trade", caller_params)
    await asyncio.sleep(0.02)  # let any pending mutator finish

    assert caller_params["amount"] == 1_000_000.0, "mutator did not run; test is vacuous"
    assert stage.evaluated == evaluated_by_stage

    # The seal verifies for exactly what the stage evaluated ...
    assert routing_seal.verify_seal(seal, "execute_trade", evaluated_by_stage)
    # ... and fails closed for the caller's mutated dict.
    with pytest.raises(SymbolicGovernorViolation):
        routing_seal.verify_seal(seal, "execute_trade", caller_params)
