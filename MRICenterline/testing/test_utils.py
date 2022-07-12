import os
from MRICenterline import CFG
from MRICenterline.app.database.openable_files import get_openable_sequences
from MRICenterline.app.database.openable_sessions import get_all_sessions
from MRICenterline.app.database.name_id import get_case_name


def generate_file_list(with_sequence: bool = False):
    """
    generates a file list for the testing tools to use. setting limit to -1 means that all available cases
    will be used
    """

    case_names = get_openable_sequences()[0]['case_name']
    case_complete_path = [os.path.join(CFG.get_folder('raw_data'), case) for case in case_names]

    if with_sequence:
        return list(zip(case_complete_path, get_openable_sequences()[0]['sequences']))
    else:
        return list(case_complete_path)


# print(generate_file_list()[47])


def generate_list_of_sessions():
    session_ids = get_all_sessions()[0]['session_id']
    case_names = get_all_sessions()[0]['case_id']

    case_complete_path = [os.path.join(CFG.get_folder('raw_data'), case) for case in case_names]

    return list(zip(session_ids, case_complete_path))


print(generate_list_of_sessions()[47])
