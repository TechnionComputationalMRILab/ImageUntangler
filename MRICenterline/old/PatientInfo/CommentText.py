"""
handles the save/load functions of the comments
"""

from glob import glob
from pathlib import Path
from datetime import datetime, timezone
import codecs  # for utf8 support / hebrew input support

import logging
logging.getLogger(__name__)


class CommentParser:
    def __init__(self, parent=None):
        self.parent = parent
        self.data_folder = parent.data_folder

        self.comment_files = [Path(fi) for fi in glob(f'{self.data_folder}/*.comment.txt')]
        self.comment_text = ""
        self.is_empty = False if len(self.comment_files) else True

        self.load_comments()

    def load_comments(self):
        # look for previous comments
        if not self.is_empty:
            logging.debug(f'{len(self.comment_files)} comments found in {self.data_folder}')

            _comment_list = []
            for fi in self.comment_files:
                with codecs.open(fi, 'r', "utf-8-sig") as f:
                    _comment_list.append(f.readlines())

            # prettify the output:
            for comment in _comment_list:
                for line in comment:
                    self.comment_text += str(line)
                self.comment_text += "\n\n"
                self.comment_text += "----------- ---------- \n"

            # self.comment_text = str(_comment_list)

        else:
            logging.info("No previous comments found")

    def save_comments(self, input_text):
        sequence = self.parent.current_sequence
        filename_timestamp = datetime.now(timezone.utc).astimezone().strftime("%d.%m.%Y__%H_%M")
        timestamp = datetime.now(timezone.utc).astimezone().strftime('%d.%m.%Y %H:%M')

        logging.info(f"Saving comment to {Path(f'{self.data_folder}/{filename_timestamp}.comment.txt')}")
        with codecs.open(Path(f'{self.data_folder}/{filename_timestamp}.comment.txt'), 'w', "utf-8-sig") as f:
            f.write(f"Sequence: {sequence}\n")
            f.write(f"Timestamp: {timestamp}\n")
            f.write("---\n")
            f.write(input_text)

    @staticmethod
    def _add_to_textbox(text, color=None):
        if color:
            out_html = f"<p><font color={color}> {text} </font></p>"
        else:
            out_html = f"<p> {text} </p>"
        return out_html

