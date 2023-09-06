\ENCODING=ISO-8859-1
\Problem name: example

Maximize
 obj1: x1 + 2 x2 + 3 x3 + x4 + [ - 33 x1 ^2 + 12 x1 * x2 - 22 x2 ^2
       + 23 x2 * x3 - 11 x3 ^2 ] / 2
Subject To
 c1: - x1 + x2 + x3 + 10 x4 <= 20
 c2: x1 - 3 x2 + x3 <= 30
 c3: x2 - 3.5 x4  = 0
Bounds
 0 <= x1 <= 40
 0 <= x4 <= 3
Generals
 x4 
End
