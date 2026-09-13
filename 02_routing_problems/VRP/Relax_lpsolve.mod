param n;
param k;

set customer:= 0..n;

param coste{i in customer, j in customer: i<>j};

var use{i in customer, j in customer: i<>j} >=0, <=1;


/* Objective function */
minimize coste_total:
         sum{i in customer, j in customer: i<>j} coste[i,j]*use[i,j];
         
#Degree constraints

#Depot
subject to out_depot:
        sum{j in customer: j>0} use[0,j] = k;
subject to in_depot:
        sum{i in customer: i>0} use[i,0] = k;

#customers
subject to in_customer{j in customer: j>0}:
        sum{i in customer: i<>j} use[i,j] = 1;
subject to out_customer{i in customer: i>0}:
        sum{j in customer: j<>i} use[i,j] = 1;


data;

param n := 6;
param k := 2;

param coste:
      0   1   2   3   4   5   6 :=
0     .   3   4   5   3   4   5
1     3   .   2   3   9   9   9
2     4   2   .   2   9   9   9
3     5   3   2   .   9   9   9
4     3   9   9   9   .   2   3
5     4   9   9   9   2   .   2
6     5   9   9   9   3   2   .;

end;