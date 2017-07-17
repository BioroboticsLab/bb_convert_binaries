import capnp

import bb_convert_binaries.helpers as helpers


class BBB_Converter(object):
    """Class to convert bbb-binaries, from one scheme to another."""

    def __init__(self, path_old_scheme=None, path_new_scheme=None):
        """Initialize BBB_Converter.

        Args:
            path_old_scheme (str): Path of the old bb_binary scheme.
            path_new_scheme (str): Path of the new bb_binary scheme.
        """
        capnp.remove_import_hook()
        if path_old_scheme is None:
            path_old_scheme = helpers.get_default_path_old_scheme()

        if path_new_scheme is None:
            path_new_scheme = helpers.get_default_path_new_scheme()

        self.old_sh = capnp.load(path_old_scheme)
        self.new_sh = capnp.load(path_new_scheme)

    def load_surveyor(self, surveyor):
        self.surveyor = surveyor

    @staticmethod
    def _fill_hive_mapped_detection(xpos, ypos, zRotation, radius):
        pass
