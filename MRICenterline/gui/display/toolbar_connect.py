from MRICenterline.app.points.status import PickerStatus, TimerStatus, PointStatus
from MRICenterline.app.gui_data_handling.case_model import CaseModel


def set_picker_status(parent: CaseModel, status: PickerStatus):
    parent.set_picker_status(status)


def save(parent: CaseModel):
    parent.save()


def calculate(parent: CaseModel, s: PointStatus):
    parent.calculate(s)


def intermediate_points(parent: CaseModel, show: bool):
    parent.intermediate_points(show)


def timer_status(parent: CaseModel, status: TimerStatus):
    parent.timer_status(status)


def undo(parent: CaseModel, undo_all: bool = False):
    parent.undo(undo_all)


def patient_info(model, parent):
    from MRICenterline.gui.metadata.dialog_box import MetadataDialogBox
    metadata = MetadataDialogBox(model=model, parent=parent)
    metadata.show()


def comment(model, parent):
    from MRICenterline.gui.comment.dialog_box import CommentDialogBox
    comment_db = CommentDialogBox(model=model, parent=parent)
    comment_db.show()
