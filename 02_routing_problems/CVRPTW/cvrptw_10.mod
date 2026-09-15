
param n;
param k;
param Q;
param M;

set node := 0..n;
set customer := 1..n;

param cost{i in node, j in node: i<>j};
param demand{i in customer};
param earliest_time{i in customer};
param latest_time{i in customer};
param service_time{i in node};

var use{i in node, j in node: i<>j} binary;
var accum_load{i in customer} >= demand[i], <= Q;
var start_time{i in node} >= 0;

/* Objective function */
minimize total_cost:
         sum{i in node, j in node: i<>j} cost[i,j]*use[i,j];
         

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
subject to load_propagation{i in customer, j in customer: i<>j}:
        accum_load[j] >= accum_load[i] + demand[j] - Q*(1-use[i,j]);

#Time window
subject to time_window_min{i in customer}:
    start_time[i] >= earliest_time[i];

subject to time_window_max{i in customer}:
    start_time[i] <= latest_time[i];

#Depot start time
subject to depot_start_time:
        start_time[0] = 0;

#Time Propagation
subject to time_propagation{i in node, j in customer: i<>j}:
        start_time[j] >= start_time[i] + service_time[i] + cost[i,j] - M*(1 - use[i,j]);



data;

param n := 10;
param k := 3;
param Q := 10;
param M := 100;


/* Customer demands */

param demand :=
1    2
2    3
3    2
4    4
5    2
6    3
7    1
8    2
9    3
10   2;


/* Service times */

param service_time :=
0    0
1    2
2    2
3    2
4    2
5    2
6    2
7    2
8    2
9    2
10   2;


/* Earliest service times */

param earliest_time :=
1     3
2     8
3    12
4     6
5    10
6    14
7    20
8     4
9     8
10   12;


/* Latest service times */

param latest_time :=
1     7
2    11
3    16
4     9
5    14
6    18
7    25
8     7
9    12
10   16;


/* Travel times */

param cost:
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