import os


stylesheet_names = {"ErrorMessage": "AlertMessage.css",
                    "Default": "DefaultBackground.css",
                    "Menu": "MenuBar.css",
                    "AddFiles": "AddFilesButton.css",
                    "Tab": "Tab.css",
                    "TabManager": "TabManager.css"}


def get_sheet_by_name(name: str):
    return get_sheet__by_path(get_CSS_directory() + os.path.sep + stylesheet_names[name])


def get_sheet__by_path(sheet_path: str):
    with open(sheet_path, 'r') as sheet_file:
        css = sheet_file.read()
    return css


def get_CSS_directory() -> str:
    script_dir = os.path.dirname(os.path.realpath(__file__))
    css_path = script_dir + os.path.sep + '..' + os.path.sep + '..' + os.path.sep + 'CSS'
    return os.path.abspath(css_path)

