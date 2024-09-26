#!/bin/bash
AOC_YEAR="$1"
AOC_DAY="$2"

export AOC_YEAR
export AOC_DAY

dd="$(printf %02d $AOC_DAY)"

touch "y$AOC_YEAR/tests/$dd"
sed "s/_YEAR_/$AOC_YEAR/; s/_DAY_/$AOC_DAY/" skeleton.py > "y$AOC_YEAR/d$dd.py"
echo -e "

def test_y${AOC_YEAR}d${dd}():
    assert get_day_result($AOC_DAY) == (0, 0)" >> "tests/test_${AOC_YEAR}.py"

git add -N "y$AOC_YEAR/tests/$dd" "y$AOC_YEAR/d$dd.py"
