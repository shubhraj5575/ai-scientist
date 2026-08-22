import json

from ais.agents.designer import ComponentBandit
from ais.agents.space import (CHAMPION_SEED_CONFIG, BASELINE_CONFIG,
                              config_uid, to_ilscfg, validate)


def test_validate_rejects_unknown_component():
    errs = validate({"not_a_component": 1})
    assert errs


def test_validate_accepts_champion_seed():
    assert validate(CHAMPION_SEED_CONFIG) == []


def test_config_uid_stable_and_order_insensitive():
    a = dict(CHAMPION_SEED_CONFIG)
    b = dict(reversed(list(CHAMPION_SEED_CONFIG.items())))
    assert config_uid(a) == config_uid(b)
    assert config_uid(a) != config_uid(BASELINE_CONFIG)


def test_to_ilscfg_roundtrip():
    cfg = dict(CHAMPION_SEED_CONFIG)
    ilscfg = to_ilscfg(cfg)
    assert ilscfg.construction == "nn"
    assert ilscfg.perturbation == "double_bridge"
    assert ilscfg.ls_operators == ("two_opt",)


def test_bandit_explores_unplayed_arms_first():
    b = ComponentBandit()
    v1, _ = b.best_value("acceptance", ["better", "sa"])
    b.update("acceptance", "better", +1.0)
    v2, s2 = b.best_value("acceptance", ["better", "sa"])
    assert v1 == "better"      # deterministic tie -> first listed arm
    assert v2 == "sa"          # unplayed arm has infinite UCB
