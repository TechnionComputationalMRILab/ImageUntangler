from MRICenterline.app.file_reader.imager import Imager
from MRICenterline.app.gui_data_handling.image_properties import ImageProperties
from MRICenterline.app.gui_data_handling.slice_loc_based_image_properties import SliceLocImageProperties

from MRICenterline import CFG


class GraphicalImager(Imager):
    def __getitem__(self, item) -> ImageProperties:
        """
        creates the associated ImageProperties, which contains the sITK image and only the necessary metadata
        to be used by GenericSequenceViewer
        """
        if isinstance(item, int):
            return self[self.get_sequences()[item]]
        else:
            z_coords = self.reader.get_z_coords(item)
            if CFG.get_testing_status("use-slice-location"):

                self.sequence = item
                self.np_array, file_list = self.reader[item]

                self.properties = SliceLocImageProperties(np_array=self.np_array,
                                                          z_coords=z_coords,
                                                          file_list=file_list)

                return self.properties
            else:
                self.sequence = item
                self.sitk_image = self.reader[item]
                self.properties = ImageProperties(self.sitk_image, z_coords=z_coords, parent=self)
                return self.properties
