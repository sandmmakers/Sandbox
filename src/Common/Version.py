import json
import pathlib
import subprocess
import sys

def gitHash():
    command = ['git', 'describe', '--always', '--dirty', '--abbrev=40', '--match=\'NoTagWithThisName\'']

    try:
        result = subprocess.run(command, capture_output=True)
    except FileNotFoundError as exception:
        raise IOError(f'Failed to find the {command[0]} executable.')
    if result.returncode != 0 or len(result.stdout) < 41:
        raise IOError('Failed to get git hash.')
    return result.stdout.decode().strip()

def _releaseFile():
    if not getattr(sys, 'frozen', False):
        return {}

    with open(pathlib.Path(sys._MEIPASS) / 'RELEASE_VERSION', 'r') as file:
        return json.load(file)

def majorVersion(): return _releaseFile().get('major')
def minorVersion(): return _releaseFile().get('minor')
def bugVersion(): return _releaseFile().get('bug')

def version():
    if None in [majorVersion(), minorVersion(), bugVersion()]:
        return None
    return f'{majorVersion()}.{minorVersion()}.{bugVersion()}'
def displayVersion():
    if version() is not None:
        return version()
    else:
        return gitHash()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser('Bed Leveler 5000 version utility')
    parserGroup = parser.add_mutually_exclusive_group(required=True)
    parserGroup.add_argument('-a', '--all', action='store_true', help='display all')
    parserGroup.add_argument('-g', '--git-hash', action='store_true', help='git hash')
    parserGroup.add_argument('-M', '--major', action='store_true', help='major version')
    parserGroup.add_argument('-m', '--minor', action='store_true', help='minor version')
    parserGroup.add_argument('-b', '--bug', action='store_true', help='bug version')
    parserGroup.add_argument('-f', '--full', action='store_true', help='full version')
    parserGroup.add_argument('-d', '--display', action='store_true', help='display version')

    args = parser.parse_args()

    try:
        if args.git_hash:
            print(gitHash())
        elif args.major:
            print(majorVersion())
        elif args.minor:
            print(minorVersion())
        elif args.bug:
            print(bugVersion())
        elif args.full:
            print(version())
        elif args.display:
            print(displayVersion())
        else:
            print(f'Git hash: {gitHash()}')
            print(f'Major: {majorVersion()}')
            print(f'Minor: {minorVersion()}')
            print(f'Bug: {bugVersion()}')
            print(f'Version: {version()}')
            print(f'Display version: {displayVersion()}')
    except IOError as exception:
        print(exception, file=sys.stderr)
        sys.exit(1)