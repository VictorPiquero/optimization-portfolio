param n;

set ciudad:= 1..n;

param coste{i in ciudad, j in ciudad: j<i};

var utilizar{i in ciudad, j in ciudad: j<i} binary;

#Objective function
minimize coste_total:
         sum{i in ciudad, j in ciudad: j<i} coste[i,j]*utilizar[i,j];

#Degree constraints
subject to entrar_salir{i in ciudad}:
        sum{j in ciudad: j<i} utilizar[i,j] +
        sum{k in ciudad: i<k} utilizar[k,i] =2;
        
#Subtours consttraints

subject to subtour_123:
        utilizar[2,1] + utilizar[3,1] + utilizar[3,2] <= 2;
subject to subtour_456:
        utilizar[5,4] + utilizar[6,4] + utilizar[6,5] <= 2;
        

data;

param n:= 6;

param coste:
      1   2   3   4   5   6 :=
2     2   .   .   .   .   .
3     2   2   .   .   .   .
4    10  10  10   .   .   .
5    10  10  10   2   .   .
6    10  10  10   2   2   .;
