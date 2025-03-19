#!/bin/bash
python3 generate_dkim_selectors.py $1 > output/dkim_$1.txt
sed -e "s/\$/._domainkey.$1/" -i output/dkim_$1.txt
../massdns/bin/massdns -r ../massdns/lists/resolvers.txt -t TXT -w output/results_$1.txt output/dkim_$1.txt
grep -B 1 "p=" output/results_$1.txt
