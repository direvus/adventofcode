#!/usr/bin/env python
import argparse
import importlib
import logging
import os
import sys

from rich import box
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table

from util import timing


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-d', '--draw', action='store_true')
    parser.add_argument('-i', '--input-file', required=False)
    parser.add_argument('year', type=int)
    parser.add_argument('day', type=int)
    args = parser.parse_args()

    console = Console()
    loglevel = 'DEBUG' if args.verbose else 'INFO'
    handler = RichHandler(markup=True)
    fmt = '%(message)s'
    logging.basicConfig(level=loglevel, format=fmt, handlers=[handler])

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

    mode = '[yellow]test[/]' if args.test else '[yellow]actual[/]'
    title = f"Executing {args.year} Day {args.day} in {mode} mode"
    retcode = 0
    try:
        with timing(title):
            infile = None
            if inpath == '-':
                infile = sys.stdin
            else:
                infile = open(inpath, 'r')
            kwargs = {}
            if args.test:
                kwargs['test'] = True
            if args.draw:
                kwargs['draw'] = True
            p1, p2 = m.run(infile, **kwargs)

        console.print()
        table = Table(
                box=box.ROUNDED,
                padding=(0, 4),
                title=f"{args.year} Day {args.day} Results",
                show_lines=True)
        table.add_column('Part')
        table.add_column('Result', justify='right', style='cyan')
        table.add_row('Part 1', str(p1))
        table.add_row('Part 2', str(p2))
        console.print(table, justify='center')
    except FileNotFoundError:
        logging.error(f"No such file '{inpath}'")
        retcode = 1
    except Exception as err:
        logging.error(f"Unexpected error '{err}' occurred", exc_info=err)
        retcode = 1
    finally:
        if infile and infile != sys.stdin:
            try:
                infile.close()
            except Exception:
                pass
        sys.exit(retcode)
