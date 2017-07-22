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
"""Module to convert the bbb-binaries from the BeesBook-Project to a new format."""
import capnp
import numpy as np

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

    def create_hive_mapping_data(self, surveyor, cam_id):
        """Allocate a HiveMappingData struct.

        The HiveMappingData struct holds the parameters for mapping image
        coordinates to world coordinates.

        Args:
            surveyor (Surveyor): Surveyor (bb_stitcher) with loaded parameters.
            cam_id (int):

        Returns: HiveMappingData

        """
        assert surveyor is not None

        params = surveyor.get_parameters()
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

    def create_hive_mapped_detection(self, surveyor, xpos, ypos, zRotation, radius, cam_id):
        """Allocate a HiveMappedDetection struct from the new bb_binary_scheme.

        Args:
            surveyor (Surveyor): Surveyor (bb_stitcher) with loaded parameters.
            xpos (float):
            ypos (float):
            zRotation (float):
            radius (int):
            cam_id (int):

        Returns: HiveMappedDetection
        """
        hmdet = self.new_sh.HiveMappedDetection.new_message()
        points, angles = surveyor.map_points_angles(
            np.float64([[xpos, ypos]]), np.array([zRotation]), cam_id
        )
        hmdet.xpos = float(points[0][0])
        hmdet.ypos = float(points[0][1])
        hmdet.zRotation = float(angles[0])
        hmdet.radius = radius * surveyor.ratio_px_mm
        return hmdet

    def create_detection_dp(self, old_dp, surveyor, cam_id):
        """Allocate a DetectionDP struct for the new bb_binary_scheme.

        This function copies the data from the 'old' detection to the 'new' detection and
        extend it with the hive mapped data.

        Args:
            old_dp (capnp.lib.capnp._DynamicStructReader): the 'old' detection.
            surveyor (Surveyor): Surveyor (bb_stitcher) with loaded parameters.
            cam_id (int):

        Returns: DetectionDP
        """
        new_dp = self.new_sh.DetectionDP.new_message()

        new_dp.idx = old_dp.idx

        new_dp.xpos = old_dp.xpos
        new_dp.ypos = old_dp.ypos

        new_dp.zRotation = old_dp.zRotation
        new_dp.yRotation = old_dp.yRotation
        new_dp.xRotation = old_dp.xRotation

        new_dp.radius = old_dp.radius

        new_dp.hiveMappedDetection = self.create_hive_mapped_detection(
            surveyor, old_dp.xpos, old_dp.ypos, old_dp.zRotation, old_dp.radius, cam_id)

        new_dp.localizerSaliency = old_dp.localizerSaliency

        new_dp.init('decodedId', len(old_dp.decodedId))
        for i, num in enumerate(old_dp.decodedId):
            new_dp.decodedId[i] = num

        new_dp.init('descriptor', len(old_dp.descriptor))
        for i, num in enumerate(old_dp.descriptor):
            new_dp.descriptor[i] = num

        return new_dp

    def create_frame(self, old_frame, surveyor, cam_id):
        """Allocate a Frame struct for the new bb_binary_scheme.

        Args:
            old_frame (capnp.lib.capnp._DynamicStructReader): the 'old' frame.
            surveyor (Surveyor): Surveyor (bb_stitcher) with loaded parameters.
            cam_id (int):

        Returns: Frame
        """
        new_frame = self.new_sh.Frame.new_message()

        new_frame.id = old_frame.id
        new_frame.dataSourceIdx = old_frame.dataSourceIdx
        new_frame.frameIdx = old_frame.frameIdx
        new_frame.timestamp = old_frame.timestamp
        new_frame.timedelta = old_frame.timedelta

        du = old_frame.detectionsUnion.which()
        if du == 'detectionsDP':
            new_frame.detectionsUnion.init(
                'detectionsDP', len(old_frame.detectionsUnion.detectionsDP)
            )
            for k, old_dp in enumerate(old_frame.detectionsUnion.detectionsDP):
                new_frame.detectionsUnion.detectionsDP[k] = self.create_detection_dp(
                    old_dp, surveyor, cam_id
                )
        elif du == 'detectionsCVP':
            raise NotImplementedError()
        elif du == 'detectionsTruth':
            raise NotImplementedError()
        else:
            raise KeyError("Type {du} not supported.".format(du=du))

        return new_frame

    def create_frameContainer(self, old_fc, surveyor):
        new_fc = self.new_sh.FrameContainer.new_message()
        new_fc.id = old_fc.id

        ## DataSource
        new_fc.init('dataSources', len(old_fc.dataSources))
        for i, ds in enumerate(old_fc.dataSources):
            new_fc.dataSources[i].idx = ds.idx
            new_fc.dataSources[i].filename = ds.filename
            new_fc.dataSources[i].videoPreviewFilename = ds.videoPreviewFilename

        new_fc.fromTimestamp = old_fc.fromTimestamp
        new_fc.toTimestamp = old_fc.toTimestamp

        new_fc.init('frames', len(old_fc.frames))
        for i, old_frame in enumerate(old_fc.frames):
            new_fc.frames[i] = self.create_frame(old_frame, surveyor, old_fc.camId)

        new_fc.camId = old_fc.camId
        new_fc.hiveId = old_fc.hiveId

        new_fc.hiveMappingData = self.create_hive_mapping_data(surveyor, old_fc.camId)

        return new_fc
