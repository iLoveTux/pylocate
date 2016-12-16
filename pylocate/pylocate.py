import os
import re
import sys
import fnmatch
import zipfile
import argparse

def _regex_matches(test, filenames, patterns):
    for filename in filenames:
        if test(p.search(filename) for p in patterns):
            yield filename

def _glob_matches(test, filenames, patterns):
    for filename in filenames:
        if test(fnmatch.fnmatch(filename, p) for p in patterns):
            yield filename


def _zip_member_matches(_zip, test, regex, patterns):
    find_matches = _regex_matches if regex else _glob_matches
    try:
        archive = zipfile.ZipFile(_zip)
    except:
        return "UNABLE TO OPEN ZIPFILE: {}...SKIPPING".format(_zip)
    members = (os.path.join(_zip, name)
                for name in archive.namelist())
    members = (member.replace("/", os.path.sep)
                for member in members)
    return (match for match in _matches(test, regex, members, patterns))


def _matches(test, regex, filenames, patterns):
    find_matches = _regex_matches if regex else _glob_matches
    return (match for match in find_matches(test, filenames, patterns))


def locate(directories=os.path.abspath('.'),
           patterns=("*", ),
           matchall=False,
           regex=False,
           examine_zips=False):
    test = all if matchall else any
    if isinstance(directories, str):
        directories = (directories, )
    if isinstance(patterns, str):
        patterns = (patterns, )
    if regex:
        patterns = tuple(map(re.compile, patterns))

    for directory in directories:
        for root, dirs, files in os.walk(directory):
            filenames = (os.path.join(root, f) for f in files)
            if examine_zips:
                zips = (f for f in filenames if f.endswith(".zip"))
                for z in zips:
                    matches = _zip_member_matches(z, test, regex, patterns)
                    for match in matches:
                        yield match
            for match in _matches(test, regex, filenames, patterns):
                yield match


def parse_args(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directories", action="append")
    parser.add_argument("-p", "--patterns", action="append")
    parser.add_argument("-a", "--matchall", action="store_true")
    parser.add_argument("-e", "--regex", action="store_true")
    parser.add_argument("-z", "--examine-zips", action="store_true")
    return parser.parse_args(argv)

def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    kwargs = vars(parse_args(argv))
    for k, v in list(kwargs.items()):
        if v is None:
            del kwargs[k]
    for filename in locate(**kwargs):
        print(filename)
