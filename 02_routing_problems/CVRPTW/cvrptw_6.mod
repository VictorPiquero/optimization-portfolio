
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

param n := 6;
param k := 2;
param Q := 8;
param M := 100;


/* Customer demands */

param demand :=
1   2
2   3
3   2
4   4
5   2
6   3;


/* Service times */

param service_time :=
0   0
1   2
2   2
3   2
4   2
5   2
6   2;


/* Earliest service times */

param earliest_time :=
1    3
2    4
3    8
4   13
5   18
6   15;


/* Latest service times */

param latest_time :=
1    6
2    7
3   11
4   16
5   22
6   19;


/* Travel times */

param cost:
      0   1   2   3   4   5   6 :=
0     .   3   4   5   4   5   6
1     3   .   3   5   8   9   9
2     4   3   .   3   8   8   9
3     5   5   3   .   9   8   8
4     4   8   8   9   .   3   5
5     5   9   8   8   3   .   3
6     6   9   9   8   5   3   .;

end;