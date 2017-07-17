import os

import bb_convert_binaries.helpers as helpers


def test_get_default_path_old_scheme():
    assert os.path.exists(helpers.get_default_path_old_scheme())


def test_get_default_path_new_scheme():
    assert os.path.exists(helpers.get_default_path_new_scheme())
