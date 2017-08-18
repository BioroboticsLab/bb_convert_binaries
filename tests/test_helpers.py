import os

import bb_convert_binaries.helpers as helpers


def test_get_default_path_old_scheme():
    assert os.path.exists(helpers.get_default_path_old_scheme())


def test_get_default_path_new_scheme():
    assert os.path.exists(helpers.get_default_path_new_scheme())


def test_replace_root_dir():
    old_root_dir = '/mnt/storage/beesbook-data-clean/pipeline_data/repo_season_2016_fixed'
    new_root_dir = '/this/is/the/new/root/dir'
    old_file_path = '/mnt/storage/beesbook-data-clean/pipeline_data/repo_season_2016_fixed/2016/' \
                    '08/01/09/20/Cam_0_2016-08-01T09:24:28.524594Z--2016-08-01T09:30:08.371296Z.bbb'
    new_path = helpers.replace_root_dir(old_root_dir, new_root_dir, old_file_path)
    res_path = '/this/is/the/new/root/dir/2016/08/01/09/20/' \
               'Cam_0_2016-08-01T09:24:28.524594Z--2016-08-01T09:30:08.371296Z.bbb'
    assert new_path == res_path


def test_create_dirs(tmpdir):
    file = '2016/08/01/09/20/Cam_0_2016-08-01T09:24:28.524594Z--2016-08-01T09:30:08.371296Z.bbb'
    path = os.path.join(str(tmpdir), file)

    helpers.create_dirs(path)
    path_dir = os.path.join(str(tmpdir), '2016/08/01/09/20/')
    assert os.path.exists(path_dir)

    helpers.create_dirs(path)
