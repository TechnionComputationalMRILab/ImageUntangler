from MRICenterline.app.file_reader.imager import Imager
from MRICenterline.app.gui_data_handling.image_properties import ImageProperties


class GraphicalImager(Imager):
    def __getitem__(self, item) -> ImageProperties:
        """
        creates the associated ImageProperties, which contains the sITK image and only the necessary metadata
        to be used by GenericSequenceViewer
        """
        if isinstance(item, int):
            return self[self.get_sequences()[item]]
        else:
            self.sequence = item
            self.sitk_image = self.reader[item]
            self.properties = ImageProperties(self.sitk_image)
            return self.properties
