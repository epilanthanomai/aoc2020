#!/bin/bash

checks=0
errors=0
failures=0

check() {
  program="$1"
  expect="$2"
  checks=$((checks + 1))
  echo -n "$program "
  output="$($program)"
  if [ $? -ne 0 ]; then
    echo E
    errors=$((errors + 1))
    return
  fi
  if [ "$output" = "$expect" ]; then
    echo .
    return
  else
    echo x
    failures=$((failures + 1))
    return
  fi
}

check "./day01.py 2" 877971
check "./day01.py 3" 203481432
check "./day02.py 1" 564
check "./day02.py 2" 325
check "./day03.py 1" 240
check "./day03.py 2" 2832009600
check "./day04.py 0" 213
check "./day04.py 1" 147
check "./day05.py max" 866
check "./day05.py open" 583
check "./day06.py any" 6662
check "./day06.py all" 3382
check "./day07.py 1" 242
check "./day07.py 2" 176035
check "./day08.py 0" 1548
check "./day08.py 1" 1375
check "./day09.py 0" 15353384
check "./day09.py 1" 2466556
check "./day10.py" 2312
check "./day10.py paths" 12089663946752
check "./day11.py near" 2251
check "./day11.py far" 2019
check "./day12.py direct" 362
check "./day12.py waypoint" 29895
check "./day13.py wait" 5257
check "./day13.py sequence" 538703333547789  # lol >1bn years
check "./day14.py 1" 13865835758282
check "./day14.py 2" 4195339838136
check "./day15.py 2020" 371
check "./day15.py 30000000" 352
check "./day16.py numbers" 23036
check "./day16.py departures" 1909224687553
check "./day17.py 3" 322
check "./day17.py 4" 2000
check "./day18.py 0" 8298263963837
check "./day18.py 1" 145575710203332
check "./day19.py" 156
check "./day19.py patch" 363
check "./day20.py corners" 28057939502729
check "./day20.py roughness" 2489
check "./day21.py safe" 2125
check "./day21.py dangerous" phc,spnd,zmsdzh,pdt,fqqcnm,lsgqf,rjc,lzvh
check "./day22.py" 33694
check "./day22.py recursive" 31835
check "./day23.py" 72496583
# check "./day23.py extended" 41785843847  # 33sec
check "./day24.py" 322
check "./day24.py 100" 3831
check "./day25.py" 16902792

echo totals
echo checks $checks
echo errors $errors
echo failures $failures
[ $errors -eq 0 -a $failures -eq 0 ]
