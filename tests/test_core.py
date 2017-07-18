import os

import numpy as np
import numpy.testing as npt
import pytest

import bb_stitcher.core as st_core
import bb_convert_binaries.core as core


@pytest.fixture
def surveyor(main_indir):
    surv = st_core.Surveyor()
    surv.load(os.path.join(main_indir, 'minimal_frame_container/surveyor_param.csv'))
    return surv


@pytest.fixture
def bbb_converter(surveyor):
    bbb_conv = core.BBB_Converter()
    return bbb_conv


def test_BBB_Converter(bbb_converter):
    pass


def test_create_hive_mapping_data(bbb_converter, surveyor):
    hmdata_left = bbb_converter.create_hive_mapping_data(surveyor, 0)
    hmdata_right = bbb_converter.create_hive_mapping_data(surveyor, 1)
    trans_matrix_left = [-0.0022398620155595797, 1.0255456751031058, 8.959450838408086,
                         -1.026839997252013, 0.009969281322362003, 4167.007420646516,
                         -4.401974722996176e-06, 3.3667549012775908e-06, 1.0176034969172618]
    trans_matrix_right = [0.03975008533654551, -1.0282426501783941, 5659.198935159065,
                          1.028378695511111, 0.008623994553813196, -3.660876363447308e-06,
                          6.130759016719913e-06, -8.457247357168554e-07, 1.002536328482415]
    npt.assert_equal(trans_matrix_left, np.array(hmdata_left.transformationMatrix))
    npt.assert_equal(trans_matrix_right, np.array(hmdata_right.transformationMatrix))

    origin = [105.93472290039062, 381.43756103515625]
    npt.assert_equal(origin, np.array(hmdata_left.origin))
    npt.assert_equal(origin, np.array(hmdata_right.origin))

    ratioPxMm = 0.0638957170731
    assert hmdata_left.ratioPxMm == ratioPxMm
    assert hmdata_right.ratioPxMm == ratioPxMm

    assert tuple(hmdata_left.frameSize) == (4000, 3000)
    assert tuple(hmdata_right.frameSize) == (4000, 3000)

    assert hmdata_left.mapsToCamId == 1
    assert hmdata_right.mapsToCamId == 0


def test_create_hive_mapped_detection(bbb_converter, surveyor):
    hmdet = bbb_converter.create_hive_mapped_detection(surveyor, 10, 10, 1, 10, 0)
    print(hmdet)
