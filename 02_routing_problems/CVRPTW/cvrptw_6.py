import gurobipy as gp
from gurobipy import GRB

# Define data

nodes = [0, 1, 2, 3, 4, 5, 6]
customers = [1, 2, 3, 4, 5, 6]

k = 2
Q = 8
M = 100

# Customer demands
demand = {
    1: 2,
    2: 3,
    3: 2,
    4: 4,
    5: 2,
    6: 3
}

# Service times
service_time = {
    0: 0,
    1: 2,
    2: 2,
    3: 2,
    4: 2,
    5: 2,
    6: 2
}

# Earliest service times
earliest_time = {
    1: 3,
    2: 4,
    3: 8,
    4: 13,
    5: 18,
    6: 15
}

# Latest service times
latest_time = {
    1: 6,
    2: 7,
    3: 11,
    4: 16,
    5: 22,
    6: 19
}

# Travel times
cost = {
    (0,1): 3, (0,2): 4, (0,3): 5, (0,4): 4, (0,5): 5, (0,6): 6,

    (1,0): 3, (1,2): 3, (1,3): 5, (1,4): 8, (1,5): 9, (1,6): 9,

    (2,0): 4, (2,1): 3, (2,3): 3, (2,4): 8, (2,5): 8, (2,6): 9,

    (3,0): 5, (3,1): 5, (3,2): 3, (3,4): 9, (3,5): 8, (3,6): 8,

    (4,0): 4, (4,1): 8, (4,2): 8, (4,3): 9, (4,5): 3, (4,6): 5,

    (5,0): 5, (5,1): 9, (5,2): 8, (5,3): 8, (5,4): 3, (5,6): 3,

    (6,0): 6, (6,1): 9, (6,2): 9, (6,3): 8, (6,4): 5, (6,5): 3
}

# Create optimization model
model = gp.Model("CVRPTW")

# Create decision variables
x = model.addVars(
    cost.keys(),
    vtype=GRB.BINARY,
    name="x"
)

u = model.addVars(
    customers,
    vtype=GRB.CONTINUOUS,
    lb=0,
    ub=Q,
    name="u"
)

t = model.addVars(
    nodes,
    vtype=GRB.CONTINUOUS,
    lb=0,
    name="t"
)

# Set objective function
model.setObjective(
    gp.quicksum(cost[i,j] * x[i,j] for i, j in cost),
    GRB.MINIMIZE
)

# Add constraints
#Depot constraints
model.addConstr(
    gp.quicksum(x[0,j] for j in customers) == k,
    name="depot_out"
)

model.addConstr(
    gp.quicksum(x[i,0] for i in customers) == k,
    name="depot_in"
)

#Customer constraints
for i in customers:
    model.addConstr(
        gp.quicksum(x[i,j] for j in nodes if j != i) == 1,
        name=f"out_degree_{i}"
    )

for j in customers:   
    model.addConstr(
        gp.quicksum(x[i,j] for i in nodes if i != j) == 1,
        name=f"in_degree_{j}"
    )

# Capacity constraints
for i in customers:
    for j in customers:
        if i != j:
            model.addConstr(
                u[j] >= u[i] + demand[j] - Q * (1 - x[i,j]),
                name=f"accum_{i}_{j}"
            )

for i in customers:
    model.addConstr(
        u[i] >= demand[i],
        name=f"min_demand_{i}"
    )

# Time window constraints
for i in customers:
    model.addConstr(
        t[i] >= earliest_time[i],
        name=f"earliest_{i}"
    )
    model.addConstr(
        t[i] <= latest_time[i],
        name=f"latest_{i}"
    )

# Time propagation constraints
for i in nodes:
    for j in customers:
        if i != j:
            model.addConstr(
                t[j] >= t[i] + service_time[i] + cost[i,j] - M * (1 - x[i,j]),
                name=f"time_{i}_{j}"
            )

# Depot time constraint
model.addConstr(
    t[0] == 0,
    name="depot_time"
)


# Solve model
model.optimize()


# Print results
if model.status == GRB.OPTIMAL:
    print("Optimal solution found")
    print(f"Optimal travel time: {model.objVal}")

    print("\nSelected arcs:")
    for i, j in cost:
        if x[i,j].X > 0.5:
            print(f"{i} -> {j}")

    print("\nAccumulated loads:")
    for i in customers:
        print(f"u[{i}] = {u[i].X:.2f}")

    print("\nService start times:")
    for i in nodes:
        print(f"t[{i}] = {t[i].X:.2f}")
