import logging
logging.getLogger(__name__)


def show_preferences_dialog(parent):
    from ..settings.dialog_box import SettingsDialogBox
    logging.debug("Preferences dialog opened")

    preferences = SettingsDialogBox(parent=parent)
    preferences.exec()
