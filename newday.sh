#!/bin/bash
#
# newday.sh YEAR DAY
#
# Set up a new puzzle day for Advent of Code.
#
# This script is meant to be *sourced* (not executed), and it will set the
# AOC_YEAR, AOC_DAY and AOC_DD environment variables, create a new test input
# file, add a test case to the test suite for the year, copy a new Python file
# from the skeleton for the day, and schedule files to be added to git.
yyyy="$1"
d="$2"
dd="$(printf %02d $d)"

export AOC_YEAR="$yyyy"
export AOC_DAY="$d"
export AOC_DD="$dd"

touch "y$yyyy/tests/$dd"
sed "s/_YEAR_/$yyyy/; s/_DAY_/$d/" skeleton.py > "y$yyyy/d$dd.py"

if ! fgrep -q "test_y${yyyy}d${dd}" "tests/test_$yyyy.py"; then
    echo -e "

def test_y${yyyy}d${dd}():
    assert get_day_result($d) == (0, 0)" >> "tests/test_${yyyy}.py"
fi

git add -N "y$yyyy/tests/$dd" "y$yyyy/d$dd.py"
