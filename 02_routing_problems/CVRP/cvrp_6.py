import gurobipy as gp
from gurobipy import GRB

# Define data

nodes = [0, 1, 2, 3, 4, 5, 6]

customers = [1, 2, 3, 4, 5, 6]

k = 2
Q = 8

demand = {
    1: 2,
    2: 3,
    3: 2,
    4: 4,
    5: 2,
    6: 3
}

cost = {
    (0, 1): 3,
    (0, 2): 4,
    (0, 3): 5,
    (0, 4): 3,
    (0, 5): 4,
    (0, 6): 5,

    (1, 0): 3,
    (1, 2): 2,
    (1, 3): 3,
    (1, 4): 9,
    (1, 5): 9,
    (1, 6): 9,

    (2, 0): 4,
    (2, 1): 2,
    (2, 3): 2,
    (2, 4): 9,
    (2, 5): 9,
    (2, 6): 9,

    (3, 0): 5,
    (3, 1): 3,
    (3, 2): 2,
    (3, 4): 9,
    (3, 5): 9,
    (3, 6): 9,

    (4, 0): 3,
    (4, 1): 9,
    (4, 2): 9,
    (4, 3): 9,
    (4, 5): 2,
    (4, 6): 3,

    (5, 0): 4,
    (5, 1): 9,
    (5, 2): 9,
    (5, 3): 9,
    (5, 4): 2,
    (5, 6): 2,

    (6, 0): 5,
    (6, 1): 9,
    (6, 2): 9,
    (6, 3): 9,
    (6, 4): 3,
    (6, 5): 2
}


# Create optimization model
model = gp.Model("CVRP")

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

# Solve model
model.optimize()


# Print results
if model.status == GRB.OPTIMAL:
    print("Optimal solution found")
    print(f"Optimal distance cost: {model.objVal}")

    for i, j in cost:
        if x[i, j].X > 0.001:
            print(f"{i} -> {j}: {x[i,j].X:.3f}")


