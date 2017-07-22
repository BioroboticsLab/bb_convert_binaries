import difflib
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


def test_create_hive_mapped_detection(bbb_converter, surveyor, min_df_cam_0, min_df_cam_1):
    hive_mapped_detections_cam_0 = []
    for f, frame in enumerate(min_df_cam_0.frames):
        for d, det in enumerate(frame.detectionsUnion.detectionsDP):
            hmdet = bbb_converter.create_hive_mapped_detection(
                surveyor, det.xpos, det.ypos, det.zRotation, det.radius, 0)
            hive_mapped_detections_cam_0.append(hmdet)

    assert 52 < hive_mapped_detections_cam_0[0].xpos < 56
    assert 100 < hive_mapped_detections_cam_0[0].ypos < 104
    assert np.deg2rad(-(180-54)) < hive_mapped_detections_cam_0[0].zRotation < np.deg2rad(-(180-58))

    assert 52 < hive_mapped_detections_cam_0[1].xpos < 56
    assert 120 < hive_mapped_detections_cam_0[1].ypos < 124
    assert np.deg2rad(- 64) < hive_mapped_detections_cam_0[1].zRotation < np.deg2rad(- 60)

    assert 52 < hive_mapped_detections_cam_0[2].xpos < 56
    assert 100 < hive_mapped_detections_cam_0[2].ypos < 104
    assert np.deg2rad(-(180-54)) < hive_mapped_detections_cam_0[2].zRotation < np.deg2rad(-(180-58))

    assert 52 < hive_mapped_detections_cam_0[3].xpos < 56
    assert 120 < hive_mapped_detections_cam_0[3].ypos < 124
    assert np.deg2rad(- 65) < hive_mapped_detections_cam_0[3].zRotation < np.deg2rad(- 60)

    hive_mapped_detections_cam_1 = []
    for f, frame in enumerate(min_df_cam_1.frames):
        for d, det in enumerate(frame.detectionsUnion.detectionsDP):
            hmdet = bbb_converter.create_hive_mapped_detection(
                surveyor, det.xpos, det.ypos, det.zRotation, det.radius, 1)
            hive_mapped_detections_cam_1.append(hmdet)

    assert 312 < hive_mapped_detections_cam_1[0].xpos < 316
    assert 194 < hive_mapped_detections_cam_1[0].ypos < 198
    assert np.deg2rad(-(180-15)) < hive_mapped_detections_cam_1[0].zRotation < np.deg2rad(-(180-20))

    assert 312 < hive_mapped_detections_cam_1[1].xpos < 316
    assert 204 < hive_mapped_detections_cam_1[1].ypos < 208
    assert np.deg2rad(- 37) < hive_mapped_detections_cam_1[1].zRotation < np.deg2rad(-34)

    assert 312 < hive_mapped_detections_cam_1[2].xpos < 316
    assert 200 < hive_mapped_detections_cam_1[2].ypos < 208
    assert np.deg2rad(- 34) < hive_mapped_detections_cam_1[2].zRotation < np.deg2rad(-28)

    assert 312 < hive_mapped_detections_cam_1[3].xpos < 316
    assert 140 < hive_mapped_detections_cam_1[3].ypos < 144
    assert np.deg2rad(180 - 58) < hive_mapped_detections_cam_1[3].zRotation < np.deg2rad(180 - 54)


def test_create_detection_dp(bbb_converter, surveyor, min_df_cam_0):
    for f, frame in enumerate(min_df_cam_0.frames):
        for d, old_det in enumerate(frame.detectionsUnion.detectionsDP):
            new_det = bbb_converter.create_detection_dp(old_det, surveyor, 0)

            old_det_str = str(old_det).splitlines(keepends=True)
            new_det_str = str(new_det).splitlines(keepends=True)
            s = difflib.SequenceMatcher(None, old_det_str, new_det_str)

            # the next both lines are just for visualisation.
            # import sys
            # sys.stdout.writelines(difflib.unified_diff(old_det_str, new_det_str, n=0))

            # 'delete' -> yposHive, xposHive (old line 3-5)
            # 'insert' -> HiveMappedDetection (new line 7-12)
            assert s.get_opcodes() == [('equal', 0, 3, 0, 3), ('delete', 3, 5, 3, 3),
                                       ('equal', 5, 9, 3, 7), ('insert', 9, 9, 7, 12),
                                       ('equal', 9, 12, 12, 15)]
