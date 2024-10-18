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

mkdir -p "y$yyyy/tests" "y$yyyy/inputs"

testsfile="tests/test_${yyyy}.py"
scriptfile="y$yyyy/d$dd.py"
testinputfile="y$yyyy/tests/$dd"

touch "$testinputfile"
if [ ! -f "$scriptfile" ]; then
    sed "s/_YEAR_/$yyyy/; s/_DAY_/$d/" skeleton.py > "$scriptfile"
fi

if ! fgrep -q "test_y${yyyy}d${dd}" "$testsfile"; then
    echo -e "

def test_y${yyyy}d${dd}():
    assert get_day_result(YEAR, $d) == (0, 0)" >> "$testsfile"
fi

git add -N "$testinputfile" "$scriptfile"
