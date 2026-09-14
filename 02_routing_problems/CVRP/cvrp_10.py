import gurobipy as gp
from gurobipy import GRB

# Define data

nodes = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

customers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

k = 3
Q = 10

demand = {
    1: 2,
    2: 3,
    3: 2,
    4: 4,
    5: 2,
    6: 3,
    7: 1,
    8: 2,
    9: 3,
    10: 2
}

cost = {
    (0,1): 3, (0,2): 4, (0,3): 5, (0,4): 6, (0,5): 7,
    (0,6): 6, (0,7): 5, (0,8): 4, (0,9): 6, (0,10): 7,

    (1,0): 3, (1,2): 2, (1,3): 3, (1,4): 7, (1,5): 8,
    (1,6): 8, (1,7): 6, (1,8): 5, (1,9): 7, (1,10): 8,

    (2,0): 4, (2,1): 2, (2,3): 2, (2,4): 6, (2,5): 7,
    (2,6): 7, (2,7): 5, (2,8): 4, (2,9): 6, (2,10): 7,

    (3,0): 5, (3,1): 3, (3,2): 2, (3,4): 5, (3,5): 6,
    (3,6): 6, (3,7): 4, (3,8): 3, (3,9): 5, (3,10): 6,

    (4,0): 6, (4,1): 7, (4,2): 6, (4,3): 5, (4,5): 2,
    (4,6): 3, (4,7): 5, (4,8): 6, (4,9): 4, (4,10): 3,

    (5,0): 7, (5,1): 8, (5,2): 7, (5,3): 6, (5,4): 2,
    (5,6): 2, (5,7): 6, (5,8): 7, (5,9): 5, (5,10): 4,

    (6,0): 6, (6,1): 8, (6,2): 7, (6,3): 6, (6,4): 3,
    (6,5): 2, (6,7): 5, (6,8): 6, (6,9): 4, (6,10): 3,

    (7,0): 5, (7,1): 6, (7,2): 5, (7,3): 4, (7,4): 5,
    (7,5): 6, (7,6): 5, (7,8): 2, (7,9): 3, (7,10): 4,

    (8,0): 4, (8,1): 5, (8,2): 4, (8,3): 3, (8,4): 6,
    (8,5): 7, (8,6): 6, (8,7): 2, (8,9): 2, (8,10): 3,

    (9,0): 6, (9,1): 7, (9,2): 6, (9,3): 5, (9,4): 4,
    (9,5): 5, (9,6): 4, (9,7): 3, (9,8): 2, (9,10): 2,

    (10,0): 7, (10,1): 8, (10,2): 7, (10,3): 6, (10,4): 3,
    (10,5): 4, (10,6): 3, (10,7): 4, (10,8): 3, (10,9): 2
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


