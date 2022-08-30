#!/bin/sh
if [[ "$TERM" =~ "linux" ]]; then
  echo jae
  /bin/echo -e "
  \e]P0121212
  \e]P1ff7c59
  \e]P248d56b
  \e]P3ffb94c
  \e]P484a7f2
  \e]P5ff66e4
  \e]P639e7d8
  \e]P7f1f1f1
  \e]P8505050
  \e]P9b51530
  \e]PA076b47
  \e]PB934305
  \e]PC10237a
  \e]PD9700b7
  \e]PE005c7d
  \e]PFb3b3b3
  "
  # get rid of artifacts
  clear
fi

