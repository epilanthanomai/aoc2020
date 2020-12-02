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
check "./day02.py" 564

echo totals
echo checks $checks
echo errors $errors
echo failures $failures
[ $errors -eq 0 -a $failures -eq 0 ]
