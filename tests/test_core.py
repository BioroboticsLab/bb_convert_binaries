import pytest

import bb_stitcher.core as st_core
import bb_convert_binaries.core as core


@pytest.fixture
def bbb_converter():
    return core.BBB_Converter()


def surveyor():
    surv = st_core.Surveyor()
    surv.load('./data/in/minimal_frame_container/surveyor_param.csv')


def test_BBB_Converter(bbb_converter):
    pass
