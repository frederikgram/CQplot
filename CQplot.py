import matplotlib.pyplot as plt
import sys
import os

from datetime import datetime
from typing import Iterable, Tuple
from pylint import epylint as lint

STD_BLACKLIST = ['venv']
STD_PATTERNS = ['.py', '.pyw']


def find_files(root_path: str, patterns: str=None, blacklist: list=None) -> Iterable[Tuple]:
    if patterns is None:
        patterns = ['.py', '.pyw']

    if blacklist is None:
        blacklist = ['venv']

    for file_path, subdirs, files in os.walk(root_path):
        if any(elem in file_path for elem in blacklist):
            continue

        for file in [file for file in files if any([file.endswith(pattern) for pattern in patterns])]:
            yield file_path, file


def lint_file(file_path: str) -> float:
    stdout, stderr = lint.py_run(file_path, return_std=True)
    for out in stdout:
        if "rated at " not in out:
            continue

        pylint_score = out.split('rated at ')[1].split(' (p')[0].split('/')[0]
        return float(pylint_score)


def get_last_modification_date(file_path: str) -> datetime:
    last_modified_epoch = os.path.getmtime(os.path.join(file_path))
    last_modified_datetime = datetime.fromtimestamp(last_modified_epoch)
    return last_modified_datetime


if __name__ == "__main__":

    # Run test
    # print("This file has a pylint score of: {0}/10".format(lint_file(__file__)))

    try:
        root = sys.argv[1]
    except IndexError:
        root = '.'

    for path, name in find_files(root):
        full_path = os.path.join(path, name)
        quality = lint_file(full_path)
        last_modified = get_last_modification_date(full_path)

        plt.scatter(last_modified, quality, c=[[0, 0, 0]])

        # for extra data
        quality_map = dict()
        quality_map[full_path] = (last_modified, quality)

    # Show average score
    print("Average score: ", sum([quality_map[key][1] for key in quality_map.keys()]) / len(quality_map))

    plt.xlabel("Datetime of last modification")
    plt.ylabel("pylint score out of 10")
    plt.xticks(rotation=-45)
    plt.ylim([0, 10])
    plt.show()

