import argparse
import json
import pathlib
import re
import sys

parser = argparse.ArgumentParser('Release version utility')
parser.add_argument('tag', help='version tag')
parser.add_argument('output', type=pathlib.Path, help='output directory')

args = parser.parse_args()

try:
    # Verify tag format
    if re.fullmatch(r'^v[0-9]+\.[0-9]+\.[0-9]+$', args.tag) is None:
        raise IOError(f'"{args.tag}" is not a valid tag.')

    parts = args.tag[1:].split('.')
    version = {'major': int(parts[0]),
               'minor': int(parts[1]),
               'bug': int(parts[2])}

    outputFilePath = args.output / 'RELEASE_VERSION'
    if outputFilePath.exists():
        raise IOError(f'{outputFilePath} already exists.')

    with open(outputFilePath, 'w') as file:
        json.dump(version, file)

except IOError as exception:
    print(exception, file=sys.stderr)
    sys.exit(1)