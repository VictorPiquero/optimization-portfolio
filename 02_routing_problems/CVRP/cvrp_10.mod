param n;
param k;
param Q;

set node := 0..n;
set customer := 1..n;

param coste{i in node, j in node: i<>j};
param demand{i in customer};

var use{i in node, j in node: i<>j} binary;
var accum_load{i in customer} >= demand[i], <= Q;

/* Objective function */
minimize coste_total:
         sum{i in node, j in node: i<>j} coste[i,j]*use[i,j];

#Degree constraints

#Depot
subject to out_depot:
        sum{j in customer} use[0,j] = k;
subject to in_depot:
        sum{i in customer} use[i,0] = k;

#Customer
subject to in_customer{j in customer}:
        sum{i in node: i<>j} use[i,j] = 1;
subject to out_customer{i in customer}:
        sum{j in node: j<>i} use[i,j] = 1;
        
#Demand
subject to load_lim{i in customer, j in customer: i<>j}:
        accum_load[j] >= accum_load[i] + demand[j] - Q*(1-use[i,j]);
        

data;

param n := 10;
param k := 3;
param Q := 10;

param demand :=
1   2
2   3
3   2
4   4
5   2
6   3
7   1
8   2
9   3
10  2;

param coste:
       0   1   2   3   4   5   6   7   8   9   10 :=
0      .   3   4   5   6   7   6   5   4   6   7
1      3   .   2   3   7   8   8   6   5   7   8
2      4   2   .   2   6   7   7   5   4   6   7
3      5   3   2   .   5   6   6   4   3   5   6
4      6   7   6   5   .   2   3   5   6   4   3
5      7   8   7   6   2   .   2   6   7   5   4
6      6   8   7   6   3   2   .   5   6   4   3
7      5   6   5   4   5   6   5   .   2   3   4
8      4   5   4   3   6   7   6   2   .   2   3
9      6   7   6   5   4   5   4   3   2   .   2
10     7   8   7   6   3   4   3   4   3   2   .;

end;



