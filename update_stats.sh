#!/bin/zsh
year="${$(pwd):t}"
if [[ ${year%[0-9][0-9][0-9][0-9]} != "" ]]
then
    echo "Invalid year. Please enter a year directory before running again."
    exit 0
fi
echo "Fetching stats for year $year..."
stats="$(curl -H "Cookie: session=$(cat ~/.aocf/cookie)" https://adventofcode.com/$year/leaderboard/self)"
table=$(echo "$stats" | grep -E --color "\\s*\\d{1,2}\\s+\\d{2}:\\d{2}:\\d{2}\\s+\\d+\\s+\\d+" | sed "s/^[[:space:]]*//" | gawk '
BEGIN {
    FS="   *"
    print "|Day|Part 1 Time|Part 1 Rank|Part 1 Points|Part 2 Time|Part 2 Rank|Part 2 Points|"
    print "| - | --------- | --------- | ----------- | --------- | --------- | ----------- |"
} {
    p1 = $3+0
    p2 = $6+0
    if (p1 <= 1000) {
        p1 = "**" p1 "**"
    }
    if (p2 <= 1000) {
        p2 = "**" p2 "**"
    }
    print "|**" $1 "**|" $2 "|" p1 "|" $4 "|" $5 "|" p2 "|" $7 "|"
}')

new_contents="$(gawk -v table="$table" '
BEGIN { inside = 0 }
{
    if (/<!-- START TABLE -->/) {
        print $0
        inside = 1
        print table
        next
    }
    if (/<!-- END TABLE -->/) {
        print $0
        inside = 0
        next
    }
    if (!inside) {
        print $0
    }
}
' README.md)"
echo "$new_contents" > README.md
