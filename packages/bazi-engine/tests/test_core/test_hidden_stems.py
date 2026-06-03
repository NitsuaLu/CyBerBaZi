"""Tests for HiddenStems (藏干) module."""

from bazi.core import (
    EarthlyBranch, HeavenlyStem,
    get_hidden_stems, get_main_qi,
)


class TestHiddenStems:
    def test_zi_hidden(self):
        stems = get_hidden_stems(EarthlyBranch.ZI)
        assert len(stems) == 1
        assert stems[0].stem == HeavenlyStem.GUI
        assert stems[0].qi_level == "本气"

    def test_chou_hidden(self):
        stems = get_hidden_stems(EarthlyBranch.CHOU)
        assert len(stems) == 3
        assert stems[0].stem == HeavenlyStem.JI and stems[0].qi_level == "本气"
        assert stems[1].stem == HeavenlyStem.GUI and stems[1].qi_level == "中气"
        assert stems[2].stem == HeavenlyStem.XIN and stems[2].qi_level == "余气"

    def test_yin_hidden(self):
        stems = get_hidden_stems(EarthlyBranch.YIN)
        assert stems[0].stem == HeavenlyStem.JIA  # 本气
        assert stems[1].stem == HeavenlyStem.BING  # 中气
        assert stems[2].stem == HeavenlyStem.WU    # 余气

    def test_si_hidden(self):
        stems = get_hidden_stems(EarthlyBranch.SI)
        assert stems[0].stem == HeavenlyStem.BING  # 本气
        assert stems[1].stem == HeavenlyStem.GENG  # 中气
        assert stems[2].stem == HeavenlyStem.WU    # 余气

    def test_get_main_qi(self):
        assert get_main_qi(EarthlyBranch.ZI) == HeavenlyStem.GUI
        assert get_main_qi(EarthlyBranch.WU) == HeavenlyStem.DING
        assert get_main_qi(EarthlyBranch.SHEN) == HeavenlyStem.GENG
        assert get_main_qi(EarthlyBranch.HAI) == HeavenlyStem.REN

    def test_all_branches_have_hidden_stems(self):
        for branch in EarthlyBranch:
            stems = get_hidden_stems(branch)
            assert 1 <= len(stems) <= 3
            for entry in stems:
                assert isinstance(entry.stem, HeavenlyStem)
                assert entry.qi_level in ("本气", "中气", "余气")
