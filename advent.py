#!/usr/bin/env python
import argparse
import datetime
import importlib
import logging
import os
import sys
from urllib.request import urlopen, Request

from rich import box
from rich.console import Console
from rich.logging import RichHandler
from rich.table import Table

from util import timing


MODULES = {}


def make_url(year: int, day: int) -> str:
    return f'https://adventofcode.com/{year}/day/{day}'


def make_input_url(year: int, day: int) -> str:
    return f'https://adventofcode.com/{year}/day/{day}/input'


def load_module(year, day):
    cachekey = (year, day)
    if cachekey in MODULES:
        mod = MODULES[cachekey]
        importlib.reload(mod)
        return mod

    modpath = f'y{year}.d{day:02d}'
    mod = importlib.import_module(modpath, 'adventofcode')
    MODULES[cachekey] = mod
    return mod


def download_input(year: int, day: int, filename: str):
    url = make_input_url(year, day)
    try:
        with open('.session', 'r') as fp:
            session = fp.read().strip()
    except OSError:
        raise Exception(
                "Could not load session cookie. Please ensure your session "
                "cookie is saved in the file '.session'")
    cookie = f'session={session}'
    req = Request(url, headers={'Cookie': cookie})

    with urlopen(req) as resp:
        with open(filename, 'w') as fp:
            fp.write(resp.read().decode('utf8'))


def run_day(
        year: int, day: int, input_file: str = '',
        test: bool = False, draw: bool = False) -> int:
    yeardir = f'y{year}'
    dd = f'{day:02d}'
    m = load_module(year, day)

    if input_file:
        inpath = args.input_file
    elif test:
        inpath = os.path.join(yeardir, 'examples', dd)
    else:
        inpath = os.path.join(yeardir, 'inputs', dd)

    console = Console()
    console.print()
    mode = '[yellow]test[/]' if test else '[yellow]actual[/]'
    title = f"Executing {year} Day {dd} in {mode} mode"
    retcode = 0
    try:
        with timing(title):
            infile = None
            if inpath == '-':
                infile = sys.stdin
            else:
                infile = open(inpath, 'r')
            kwargs = {}
            if test:
                kwargs['test'] = True
            if draw:
                kwargs['draw'] = True
            p1, p2 = m.run(infile, **kwargs)

        console.print()
        table = Table(
                box=box.ROUNDED,
                padding=(0, 4),
                title=f"{year} Day {dd} Results",
                show_lines=True)
        table.add_column('Part')
        table.add_column('Result', justify='right', style='cyan')
        table.add_row('Part 1', str(p1))
        table.add_row('Part 2', str(p2))
        console.print(table)
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
        return retcode


def configure_logging(verbose: bool = False):
    loglevel = 'DEBUG' if verbose else 'INFO'
    handler = RichHandler(markup=True)
    fmt = '%(message)s'
    logging.basicConfig(
            level=loglevel,
            datefmt='%S',
            force=True,
            format=fmt,
            handlers=[handler])


def print_config_table(
        console: Console, year: int, day: int, verbose: bool, draw: bool):
    url = f'https://adventofcode.com/{year}/day/{day}'
    table = Table(
            box=box.ROUNDED,
            padding=(0, 4),
            title=f"Configuration",
            show_lines=True)
    table.add_column('Setting')
    table.add_column('Value', style='cyan')
    table.add_row('Year', str(year))
    table.add_row('Day', f'{day:02d}')
    table.add_row('URL', f'[link={url}]{url}[/link]')
    table.add_row('Logging level', '[red]Verbose[/]' if verbose else 'Normal')
    table.add_row('Visualisations enabled', '[green]Yes[/]' if draw else '[red]No[/]')

    console.print()
    console.print(table)
    console.print()


def run_interactive(
        year: int = None, day: int = None,
        verbose: bool = False, draw: bool = False):
    console = Console()
    title = (
            r"              _                 _            __    _____          _       ",
            r"     /\      | |               | |          / _|  / ____|        | |      ",
            r"    /  \   __| |_   _____ _ __ | |_    ___ | |_  | |     ___   __| | ___  ",
            r"   / /\ \ / _` \ \ / / _ \ '_ \| __|  / _ \|  _| | |    / _ \ / _` |/ _ \ ",
            r"  / ____ \ (_| |\ V /  __/ | | | |_  | (_) | |   | |___| (_) | (_| |  __/ ",
            r" /_/    \_\__,_| \_/ \___|_| |_|\__|  \___/|_|    \_____\___/ \__,_|\___| ",
            r"",
            )
    console.print('[bold yellow]' + '\n'.join(title) + '[/]')

    if year is None:
        # Infer from the current date
        today = datetime.date.today()
        year = today.year if today.month == 12 else today.year - 1

    if day is None:
        today = datetime.date.today()
        day = today.day

    print_config_table(console, year, day, verbose, draw)

    while True:
        choices = 'RTDVSQL'
        prompt = (
                ' [blue]|[/] '.join((
                    r'[yellow]\[R][/]un',
                    r'[yellow]\[T][/]est',
                    r'[yellow]\[S][/]elect year and day',
                    r'[yellow]\[L][/]oad input',
                    r'[yellow]\[Q][/]uit',
                    )) + '\n'
                r'Toggle modes: [yellow]\[D][/]rawing [blue]|[/] '
                r'[yellow]\[V][/]erbose logging [yellow]>[/] '
                )
        console.print()
        choice = console.input(prompt)[:1].upper()

        while choice not in choices:
            console.print(f':x: [red]"{choice}" is not a valid selection![/]')
            console.print()
            choice = console.input(prompt)[:1].upper()

        console.print()
        if choice == 'Q':
            console.print(':wave:\n')
            break

        elif choice == 'V':
            verbose = not verbose
            configure_logging(verbose)
            label = 'verbose' if verbose else 'normal'
            print_config_table(console, year, day, verbose, draw)
            console.print(f':white_check_mark: OK, logging level is now [green]{label}[/]')

        elif choice == 'D':
            draw = not draw
            label = 'enabled' if draw else 'disabled'
            print_config_table(console, year, day, verbose, draw)
            console.print(f':white_check_mark: OK, drawing is now [green]{label}[/]')

        elif choice == 'R':
            # Run in actual mode
            run_day(year, day, None, False, draw)

        elif choice == 'T':
            # Run in test mode
            run_day(year, day, None, True, draw)

        elif choice == 'L':
            # Download puzzle input
            filename = os.path.join(f'y{year}', 'inputs', f'{day:02d}')
            if os.path.exists(filename):
                console.print(
                        f'\n:x: Input file {filename} already exists, '
                        'not downloading it again.')
                continue

            if not os.path.exists('.session'):
                console.print(
                        '\n:x: Session cookie file .session does not exist, '
                        'please create this file before trying again.')
                continue

            try:
                download_input(year, day, filename)
                console.print(
                        '\n:white_check_mark: OK, it was downloaded :thumbs_up:')
            except Exception as e:
                console.print(
                        f'\n:x: Download failed: {e}')

        elif choice == 'S':
            # Select year and day
            value = console.input(f'Select year: \\[[blue]{year}[/]] [yellow]>[/] ')
            if value != '':
                try:
                    value = int(value)
                    current_year = datetime.date.today().year
                    if value < 2015 or value > current_year:
                        console.print(
                                f'\n:x: Enter a year number between 2015 and {current_year}.')
                        continue
                except ValueError:
                    console.print('\n:x: Yeah, nah.')
                    continue
                year = value

            value = console.input(f'Select day: \\[[blue]{day}[/]] [yellow]>[/] ')
            if value != '':
                try:
                    value = int(value)
                    if value < 1 or value > 25:
                        console.print(
                                f'\n:x: Enter a day number between 1 and 25.')
                        continue
                except ValueError:
                    console.print('\n:x: Yeah, nah.')
                    continue
                day = value

            console.print()
            console.print(f':white_check_mark: OK, selected [green]{year} day {day}[/]')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='store_true')
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-d', '--draw', action='store_true')
    parser.add_argument('-i', '--input-file', required=False)
    parser.add_argument('year', type=int, nargs='?')
    parser.add_argument('day', type=int, nargs='?')
    args = parser.parse_args()

    configure_logging(args.verbose)

    if args.year and args.day:
        retcode = run_day(
                args.year, args.day, args.input_file, args.test, args.draw)
        sys.exit(retcode)
    else:
        run_interactive(args.year, args.day, args.verbose, args.draw)
