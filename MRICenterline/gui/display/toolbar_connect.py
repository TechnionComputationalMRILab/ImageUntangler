from MRICenterline.app.points.status import PickerStatus, PointStatus
from MRICenterline.app.gui_data_handling.case_model import CaseModel
from MRICenterline.app.points.point_fill import PointFillType


def set_fill_type(parent: CaseModel, fill_type: PointFillType):
    parent.set_fill_type(fill_type)


def set_picker_status(parent: CaseModel, status: PickerStatus):
    parent.set_picker_status(status)


def save(parent: CaseModel, comment_text: str = ""):
    parent.comment_text = comment_text
    parent.save()


def calculate(parent: CaseModel, s: PointStatus, parent_widget=None):
    return parent.calculate(s, parent_widget)


def intermediate_points(parent: CaseModel, show: bool):
    parent.intermediate_points(show)


def timer_status(parent: CaseModel, status):
    parent.timer_status(status)


def undo(parent: CaseModel, undo_all: bool = False):
    parent.undo(undo_all)


def patient_info(model, parent):
    from MRICenterline.gui.metadata.dialog_box import MetadataDialogBox
    metadata = MetadataDialogBox(model=model, parent=parent)
    metadata.exec()


def find_point(model, s):
    model.find_point()


def export(model, parent):
    from MRICenterline.gui.export.dialog_box import ExportDialogBox
    export_db = ExportDialogBox(model=model, parent=parent)
    export_db.show()


def toggle_mpr_marker(model, show: bool):
    model.toggle_mpr_marker_visibility(show)


def pick_point_pair(model):
    model.pick_point_pair()


def edit_points(model, s):
    model.edit_points()
