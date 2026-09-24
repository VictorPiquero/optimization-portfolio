
param n;
param k;
param Q;
param M;

set node := 0..n;
set customer := 1..n;

param cost{i in node, j in node: i<>j};
param demand{i in customer};
param earliest_time{i in customer};
param latest_time{i in node};
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


# Depot time window constraint
subject to depot_time_window{i in customer}:
        start_time[i] + service_time[i] + cost[i,0] <= latest_time[0] + M*(1 - use[i,0]);

end;
