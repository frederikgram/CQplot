""" Plots a given codebases' pylint score over time """

import os
import sys
from datetime import datetime
from typing import Iterable, Tuple
from pylint import epylint as lint
import matplotlib.pyplot as plt


STD_BLACKLIST = ['venv']
STD_PATTERNS = ['.py', '.pyw']


def find_files(root_path: str, patterns: str = None, blacklist: list = None) -> Iterable[Tuple]:
    """
    Yields all files which whos root is root_path, and fits into patterns and blacklist filters
    :param root_path: D
    :param patterns: (optional) List of file extensions DEFAULT = ['.py', '.pyw']
    :param blacklist: (optional) List of strings that if in path, skips it. DEFAULT = ['venv']
    :return: Iterable of tuples, (file_path, file_name)
    """

    if patterns is None:
        patterns = STD_PATTERNS

    if blacklist is None:
        blacklist = STD_BLACKLIST

    for file_path, _, files in os.walk(root_path):
        if any(elem in file_path for elem in blacklist):
            continue

        filtered_files = filter(lambda _file:
                                any([_file.endswith(pattern) for pattern in patterns]),
                                files)

        for file in filtered_files:
            yield file_path, file


def lint_file(file_path: str) -> float:
    """
    Runs pylinter on a given file, and outputs the score as a float
    :param file_path: path of file ot lint
    :return: pylint score as float
    """
    stdout, stderr = lint.py_run(file_path, return_std=True)
    for out in stdout:
        if "rated at " not in out:
            continue

        pylint_score = out.split('rated at ')[1].split(' (p')[0].split('/')[0]
        return float(pylint_score)

    # Print error if no score is found
    print(list(stderr) or "Could not lint {0}".format(file_path))


def get_last_modification_date(file_path: str) -> datetime:
    """
    Gets the last date of modification for a file, and outputs it as a datetime object
    :param file_path: path of file ot lint
    :return: datetime object of last modification date
    """
    last_modified_epoch = os.path.getmtime(os.path.join(file_path))
    return datetime.fromtimestamp(last_modified_epoch)


if __name__ == "__main__":

    # Run score example
    print("This file has a pylint score of: {0}/10".format(lint_file(__file__)))

    try:
        ROOT_PATH = sys.argv[1]
    except IndexError:
        ROOT_PATH = '.'

    QUALITY_MAP = dict()

    for path, name in find_files(ROOT_PATH):
        full_path = os.path.join(path, name)
        quality = lint_file(full_path)
        last_modified = get_last_modification_date(full_path)

        plt.scatter(last_modified, quality, c=[[0, 0, 0]])

        # for extra data
        QUALITY_MAP[full_path] = (last_modified, quality)

    # Show average score
    print("Average score: ",
          sum([QUALITY_MAP[key][1] for key in QUALITY_MAP]) / len(QUALITY_MAP))

    plt.xlabel("Datetime of last modification")
    plt.ylabel("pylint score out of 10")
    plt.xticks(rotation=-45)
    plt.ylim([0, 10])
    plt.show()
