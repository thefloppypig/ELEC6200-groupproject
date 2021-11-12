#!/bin/bash

# Here we make use of bash direct array assignment
A0=($(sed '2q;d' /proc/stat))
A1=($(sed '3q;d' /proc/stat))
A2=($(sed '4q;d' /proc/stat))
A3=($(sed '5q;d' /proc/stat))
# user         + nice     + system   + idle
B0=$((${A0[1]} + ${A0[2]} + ${A0[3]} + ${A0[4]}))
B1=$((${A1[1]} + ${A1[2]} + ${A1[3]} + ${A1[4]}))
B2=$((${A2[1]} + ${A2[2]} + ${A2[3]} + ${A2[4]}))
B3=$((${A3[1]} + ${A3[2]} + ${A3[3]} + ${A3[4]}))
sleep 0.1
C0=($(sed '2q;d' /proc/stat))
C1=($(sed '3q;d' /proc/stat))
C2=($(sed '4q;d' /proc/stat))
C3=($(sed '5q;d' /proc/stat))
# user         + nice     + system   + idle
D0=$((${C0[1]} + ${C0[2]} + ${C0[3]} + ${C0[4]}))
D1=$((${C1[1]} + ${C1[2]} + ${C1[3]} + ${C1[4]}))
D2=$((${C2[1]} + ${C2[2]} + ${C2[3]} + ${C2[4]}))
D3=$((${C3[1]} + ${C3[2]} + ${C3[3]} + ${C3[4]}))
# cpu usage per core
E0=$(((100 * (B0 - D0 - ${A0[4]} + ${C0[4]})) / (B0 - D0)))
E1=$(((100 * (B1 - D1 - ${A1[4]} + ${C1[4]})) / (B1 - D1)))
E2=$(((100 * (B2 - D2 - ${A2[4]} + ${C2[4]})) / (B2 - D2)))
E3=$(((100 * (B3 - D3 - ${A3[4]} + ${C3[4]})) / (B3 - D3)))

echo $E0, $E1, $E2, $E3
