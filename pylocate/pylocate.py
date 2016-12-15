import os
import re
import sys
import fnmatch
import zipfile
import argparse

def locate(directories=os.path.abspath('.'), patterns=("*", ), matchall=False, regex=False, examine_zips=False):
    test = all if matchall else any
    if isinstance(patterns, str):
        patterns = (patterns, )
    if isinstance(directories, str):
        directories = (directories, )
    if regex:
        patterns = tuple(re.compile(pattern) for pattern in patterns)
    for directory in directories:
        for root, dirs, files in os.walk(directory):
            for filename in (os.path.join(root, f) for f in files):
                if filename.endswith(".zip") and examine_zips:
                    try:
                        archive = zipfile.ZipFile(filename)
                    except:
                        yield "UNABLE TO OPEN ZIPFILE: {}...SKIPPING".format(filename)
                        continue
                    for name in archive.namelist():
                        member_name = os.path.join(root, filename, name)
                        member_name = member_name.replace("/", os.path.sep)
                        if regex:
                            if test(p.search(member_name) is not None for p in patterns):
                                yield member_name
                        else:
                            if test(fnmatch.fnmatch(member_name, p) for p in patterns):
                                yield member_name
                if regex:
                    if test(p.search(filename) is not None for p in patterns):
                        yield os.path.join(root, filename)
                else:
                    if test(fnmatch.fnmatch(filename, p) for p in patterns):
                        yield os.path.join(root, filename)


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
