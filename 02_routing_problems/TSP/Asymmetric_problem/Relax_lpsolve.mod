param n;

set ciudad:= 1..n;

param coste{i in ciudad, j in ciudad: i<>j};

var utilizar{i in ciudad, j in ciudad: i<>j} >= 0, <= 1;

/* Objective function */
minimize coste_total:
         sum{i in ciudad, j in ciudad: i<>j} coste[i,j]*utilizar[i,j];
         
#Degree constraints
subject to salir{i in ciudad}:
        sum{j in ciudad: j<>i} utilizar[i,j] =1;
        
subject to entrar{j in ciudad}:
        sum{i in ciudad: i<>j} utilizar[i,j] =1;

data;

param n:= 6;

param coste:
      1   2   3   4   5   6 :=
1     .   2   8  10  10  10
2     8   .   2  10  10  10
3     2   8   .  10  10  10
4    10  10  10   .   2   8
5    10  10  10   8   .   2
6    10  10  10   2   8   .;

