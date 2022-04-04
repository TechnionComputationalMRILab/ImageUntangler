from MRICenterline.app.file_reader.imager import Imager


def run_metadata_sequence_scan(folders, parent_widget=None):
    num_folders = len(folders)
    for index, folder in enumerate(folders):
        if parent_widget:
            parent_widget.add_to_textbox(f"[{1 + index} / {num_folders}] Reading {folder}")

        try:
            imager = Imager(folder)
        except NotImplementedError:
            parent_widget.add_to_textbox(f"{folder} is either not supported or has no MRI images.", color='red')
        else:
            if parent_widget:
                parent_widget.add_to_textbox(f"Folder is {imager.file_type} | {len(imager)} sequences found")

    parent_widget.add_to_textbox(f"Done! You may close.")
