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
