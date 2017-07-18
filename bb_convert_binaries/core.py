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
        self.surveyor = None

    def load_surveyor(self, surveyor):
        self.surveyor = surveyor

    def create_hive_mapping_data(self, cam_id):
        assert self.surveyor is not None

        params = self.surveyor.get_parameters()
        assert cam_id in [params.cam_id_left, params.cam_id_right]

        hmdata = self.new_sh.HiveMappingData.new_message()

        hmdata.init('transformationMatrix', 9)
        hmdata.init('frameSize', 2)
        hmdata.init('origin', 2)
        hmdata.origin = params.origin.tolist()
        hmdata.ratioPxMm = params.ratio_px_mm

        if cam_id == params.cam_id_left:

            hmdata.transformationMatrix = params.homo_left.flatten().tolist()

            for i in range(2):
                hmdata.frameSize[i] = params.size_left[i]

            hmdata.mapsToCamId = params.cam_id_right

        else:
            hmdata.transformationMatrix = params.homo_right.flatten().tolist()

            for i in range(2):
                hmdata.frameSize[i] = params.size_right[i]

            hmdata.mapsToCamId = params.cam_id_left

        return hmdata
