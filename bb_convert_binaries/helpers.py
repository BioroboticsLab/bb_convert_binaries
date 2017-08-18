#  Licensed under the Apache License, Version 2.0 (the "License"); you may
#  not use this file except in compliance with the License. You may obtain
#  a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#  WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#  License for the specific language governing permissions and limitations
#  under the License.
"""This module provides various helper functions."""
import os


def get_default_path_old_scheme():
    """Return the default config."""
    path_schema = os.path.join(os.path.dirname(__file__), 'bb_binary_schemas',
                               'bb_binary_scheme_old.capnp')
    return path_schema


def get_default_path_new_scheme():
    """Return the default config."""
    path_schema = os.path.join(os.path.dirname(__file__), 'bb_binary_schemas',
                               'bb_binary_scheme_new.capnp')
    return path_schema


def replace_root_dir(old_root_dir, new_root_dir, old_file_path):
    """Return new file path, which is a combination of new_root_dir and old_file_path.

    Args:
        old_root_dir(str): Root dir to be replaced.
        new_root_dir(str): This is new root dir, which would replace old root dir.
        old_file_path(str): Path with old root dir.

    Returns: new file path.
    """
    rel_file_path = old_file_path[len(old_root_dir) + 1:]
    return os.path.join(new_root_dir, rel_file_path)
