import os
import os.path

import capnp
import pytest

import bb_convert_binaries.helpers as helpers


# add marker for incremental testing
# http://doc.pytest.org/en/latest/example/simple.html#incremental-testing-test-steps


def pytest_runtest_makereport(item, call):
    if "incremental" in item.keywords:
        if call.excinfo is not None:
            parent = item.parent
            parent._previousfailed = item


def pytest_runtest_setup(item):
    if "incremental" in item.keywords:
        previousfailed = getattr(item.parent, "_previousfailed", None)
        if previousfailed is not None:
            pytest.xfail("previous test failed (%s)" % previousfailed.name)


test_dir = os.path.dirname(__file__)


@pytest.fixture
def main_indir():
    return os.path.join(test_dir, 'data', 'in')


@pytest.fixture
def main_outdir():
    out_path = os.path.join(test_dir, 'data', 'out')
    if not os.path.exists(out_path):
        os.makedirs(out_path)
    return out_path


def min_df(main_indir, path_bbb):
    capnp.remove_import_hook()
    path_old_scheme = helpers.get_default_path_old_scheme()
    old_sh = capnp.load(path_old_scheme)
    path = os.path.join(main_indir, path_bbb)
    with open(path, 'rb') as old_bbb:
        old_fc = old_sh.FrameContainer.read(old_bbb)
    return old_fc


@pytest.fixture
def min_df_cam_0(main_indir):
    path = os.path.join(main_indir,
                        'minimal_frame_container/bb_binaries/'
                        'Cam_0_2016-07-31T00:01:38.159691Z--2016-07-31T00:07:18.006892Z_min.bbb')
    return min_df(main_indir, path)


@pytest.fixture
def min_df_cam_1(main_indir):
    path = os.path.join(main_indir,
                        'minimal_frame_container/bb_binaries/'
                        'Cam_1_2016-07-31T00:02:08.738354Z--2016-07-31T00:07:48.569969Z.bbb')
    return min_df(main_indir, path)
