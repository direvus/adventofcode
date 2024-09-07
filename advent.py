#!/usr/bin/env python
import argparse
import importlib
import os
import sys

from rich import print

from util import timing


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='store_true')
    parser.add_argument('-i', '--input-file', required=False)
    parser.add_argument('year', type=int)
    parser.add_argument('day', type=int)
    args = parser.parse_args()

    year = f'y{args.year}'
    day = f'{args.day:02d}'
    modpath = f'{year}.d{day}'
    m = importlib.import_module(modpath, 'adventofcode')

    if args.input_file:
        inpath = args.input_file
    elif args.test:
        inpath = os.path.join(year, 'tests', day)
    else:
        inpath = os.path.join(year, 'inputs', day)

    mode = '[orange]test[/]' if args.test else '[orange]actual[/]'
    print(f"Executing {args.year} Day {args.day} in {mode} mode\n")
    with timing('\n'):
        try:
            if inpath == '-':
                infile = sys.stdin
            else:
                infile = open(inpath, 'r')
            p1, p2 = m.run(infile, test=args.test)
            print(f"Part 1 => {p1}")
            print(f"Part 2 => {p2}")
        finally:
            if inpath != '-':
                infile.close()
