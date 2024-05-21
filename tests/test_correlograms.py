
"""Tests of correlograms for `pynapple` package."""

import pynapple as nap
import numpy as np
import pandas as pd
import pytest
from itertools import combinations


def test_cross_correlogram():
    t1 = np.array([0])
    t2 = np.array([1])
    cc, bincenter = nap.process.correlograms._cross_correlogram(t1, t2, 1, 100)
    np.testing.assert_approx_equal(cc[101], 1.0)

    cc, bincenter = nap.process.correlograms._cross_correlogram(t2, t1, 1, 100)
    np.testing.assert_approx_equal(cc[99], 1.0)

    t1 = np.array([0])
    t2 = np.array([100])
    cc, bincenter = nap.process.correlograms._cross_correlogram(t1, t2, 1, 100)
    np.testing.assert_approx_equal(cc[200], 1.0)

    t1 = np.array([0, 10])
    cc, bincenter = nap.process.correlograms._cross_correlogram(t1, t1, 1, 100)
    np.testing.assert_approx_equal(cc[100], 1.0)
    np.testing.assert_approx_equal(cc[90], 0.5)
    np.testing.assert_approx_equal(cc[110], 0.5)

    np.testing.assert_array_almost_equal(bincenter, np.arange(-100, 101))

    for t in [100, 200, 1000]:
        np.testing.assert_array_almost_equal(
            nap.process.correlograms._cross_correlogram(np.arange(0, t), np.arange(0, t), 1, t)[0],
            np.hstack(
                (np.arange(0, 1, 1 / t), np.ones(1), np.arange(0, 1, 1 / t)[::-1])
            ),
        )


@pytest.mark.parametrize(
    "group",
    [
        nap.TsGroup(
            {
                0: nap.Ts(t=np.arange(0, 100)),
                1: nap.Ts(t=np.arange(0, 100)),
                2: nap.Ts(t=np.array([0, 10])),
                3: nap.Ts(t=np.arange(0, 200)),
            }
        )
    ],
)
class Test_Correlograms:
    def test_autocorrelogram(self, group):
        cc = nap.compute_autocorrelogram(group, 1, 100, norm=False)
        assert isinstance(cc, pd.DataFrame)
        assert list(cc.keys()) == list(group.keys())
        np.testing.assert_array_almost_equal(cc.index.values, np.arange(-100, 101, 1))
        np.testing.assert_array_almost_equal(
            cc[0].values,
            np.hstack(
                (np.arange(0, 1, 1 / 100), np.zeros(1), np.arange(0, 1, 1 / 100)[::-1])
            ),
        )
        np.testing.assert_array_almost_equal(
            cc[0].values,
            np.hstack(
                (np.arange(0, 1, 1 / 100), np.zeros(1), np.arange(0, 1, 1 / 100)[::-1])
            ),
        )
        tmp = np.zeros(len(cc))
        tmp[[90, 110]] = 0.5
        np.testing.assert_array_almost_equal(tmp, cc[2])

    def test_autocorrelogram_error(self, group):
        with pytest.raises(RuntimeError) as e_info:
            nap.compute_autocorrelogram([1,2,3], 1, 100, norm=False)
        assert str(e_info.value) == "Unknown format for group"

    def test_autocorrelogram_with_ep(self, group):
        ep = nap.IntervalSet(start=0, end=99)
        cc = nap.compute_autocorrelogram(group, 1, 100, ep=ep, norm=False)
        np.testing.assert_array_almost_equal(cc[0].values, cc[3].values)

    def test_autocorrelogram_with_norm(self, group):
        cc = nap.compute_autocorrelogram(group, 1, 100, norm=False)
        cc2 = nap.compute_autocorrelogram(group, 1, 100, norm=True)
        tmp = group._metadata["rate"].values.astype("float")
        np.testing.assert_array_almost_equal(cc / tmp, cc2)

    def test_autocorrelogram_time_units(self, group):
        cc = nap.compute_autocorrelogram(group, 1, 100, time_units="s")
        cc2 = nap.compute_autocorrelogram(group, 1 * 1e3, 100 * 1e3, time_units="ms")
        cc3 = nap.compute_autocorrelogram(group, 1 * 1e6, 100 * 1e6, time_units="us")
        pd.testing.assert_frame_equal(cc, cc2)
        pd.testing.assert_frame_equal(cc, cc3)

    def test_crosscorrelogram(self, group):
        cc = nap.compute_crosscorrelogram(group, 1, 100, norm=False)
        assert isinstance(cc, pd.DataFrame)
        assert list(cc.keys()) == list(combinations(group.keys(), 2))
        np.testing.assert_array_almost_equal(cc.index.values, np.arange(-100, 101, 1))
        np.testing.assert_array_almost_equal(
            cc[(0, 1)].values,
            np.hstack(
                (np.arange(0, 1, 1 / 100), np.ones(1), np.arange(0, 1, 1 / 100)[::-1])
            ),
        )

    def test_crosscorrelogram_reverse(self, group):
        cc = nap.compute_crosscorrelogram(group, 1, 100, reverse=True)
        assert isinstance(cc, pd.DataFrame)

        from itertools import combinations

        pairs = list(combinations(group.index, 2))
        pairs = list(map(lambda n: (n[1], n[0]), pairs))

        assert pairs == list(cc.keys())

    def test_crosscorrelogram_with_ep(self, group):
        ep = nap.IntervalSet(start=0, end=99)
        cc = nap.compute_crosscorrelogram(group, 1, 100, ep=ep, norm=False)
        np.testing.assert_array_almost_equal(cc[(0, 1)].values, cc[(0, 3)].values)

    def test_crosscorrelogram_with_norm(self, group):
        cc = nap.compute_crosscorrelogram(group, 1, 100, norm=False)
        cc2 = nap.compute_crosscorrelogram(group, 1, 100, norm=True)
        tmp = group._metadata["rate"].values.astype("float")
        tmp = tmp[[t[1] for t in cc.columns]]
        np.testing.assert_array_almost_equal(cc / tmp, cc2)

    def test_crosscorrelogram_time_units(self, group):
        cc = nap.compute_crosscorrelogram(group, 1, 100, time_units="s")
        cc2 = nap.compute_crosscorrelogram(group, 1 * 1e3, 100 * 1e3, time_units="ms")
        cc3 = nap.compute_crosscorrelogram(group, 1 * 1e6, 100 * 1e6, time_units="us")
        pd.testing.assert_frame_equal(cc, cc2)
        pd.testing.assert_frame_equal(cc, cc3)

    def test_crosscorrelogram_error(self, group):
        with pytest.raises(RuntimeError) as e_info:
            nap.compute_crosscorrelogram([1,2,3], 1, 100)
        assert str(e_info.value) == "Unknown format for group"

    def test_crosscorrelogram_with_tuple(self, group):
        from itertools import product
        groups = (group[[0,1]], group[[2,3]])
        cc = nap.compute_crosscorrelogram(groups, 1, 100, norm=False)

        assert isinstance(cc, pd.DataFrame)
        assert list(cc.keys()) == list(product(groups[0].keys(), groups[1].keys()))
        np.testing.assert_array_almost_equal(cc.index.values, np.arange(-100, 101, 1))

        cc2 = nap.compute_crosscorrelogram(group[[0,2]], 1, 100, norm=False)
        np.testing.assert_array_almost_equal(
            cc[(0, 2)].values,
            cc2[(0,2)].values
            )

    def test_eventcorrelogram(self, group):
        cc = nap.compute_eventcorrelogram(group, group[0], 1, 100, norm=False)
        cc2 = nap.compute_crosscorrelogram(group, 1, 100, norm=False)
        assert isinstance(cc, pd.DataFrame)
        assert list(cc.keys()) == list(group.keys())
        np.testing.assert_array_almost_equal(cc[1].values, cc2[(0, 1)].values)

    def test_eventcorrelogram_with_ep(self, group):
        ep = nap.IntervalSet(start=0, end=99)
        cc = nap.compute_eventcorrelogram(group, group[0], 1, 100, ep=ep, norm=False)
        cc2 = nap.compute_crosscorrelogram(group, 1, 100, ep=ep, norm=False)
        assert isinstance(cc, pd.DataFrame)
        assert list(cc.keys()) == list(group.keys())
        np.testing.assert_array_almost_equal(cc[1].values, cc2[(0, 1)].values)

    def test_eventcorrelogram_with_norm(self, group):
        cc = nap.compute_eventcorrelogram(group, group[0], 1, 100, norm=False)
        cc2 = nap.compute_eventcorrelogram(group, group[0], 1, 100, norm=True)
        # tmp = group._metadata["rate"].values.astype("float")
        tmp = group.get_info("rate").values
        np.testing.assert_array_almost_equal(cc / tmp, cc2)

    def test_eventcorrelogram_time_units(self, group):
        cc = nap.compute_eventcorrelogram(group, group[0], 1, 100, time_units="s")
        cc2 = nap.compute_eventcorrelogram(
            group, group[0], 1 * 1e3, 100 * 1e3, time_units="ms"
        )
        cc3 = nap.compute_eventcorrelogram(
            group, group[0], 1 * 1e6, 100 * 1e6, time_units="us"
        )
        pd.testing.assert_frame_equal(cc, cc2)
        pd.testing.assert_frame_equal(cc, cc3)

    def test_eventcorrelogram_error(self, group):
        with pytest.raises(RuntimeError) as e_info:
            nap.compute_eventcorrelogram([1,2,3], group[0], 1, 100)
        assert str(e_info.value) == "Unknown format for group"
