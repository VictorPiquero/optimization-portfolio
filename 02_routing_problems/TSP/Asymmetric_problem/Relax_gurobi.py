# Import libraries
import gurobipy as gp
from gurobipy import GRB

# Define data
cities = range(1, 7)

cost = {
    (1, 2): 2,
    (1, 3): 8,
    (1, 4): 10,
    (1, 5): 10,
    (1, 6): 10,

    (2, 1): 8,
    (2, 3): 2,
    (2, 4): 10,
    (2, 5): 10,
    (2, 6): 10,

    (3, 1): 2,
    (3, 2): 8,
    (3, 4): 10,
    (3, 5): 10,
    (3, 6): 10,

    (4, 1): 10,
    (4, 2): 10,
    (4, 3): 10,
    (4, 5): 2,
    (4, 6): 8,

    (5, 1): 10,
    (5, 2): 10,
    (5, 3): 10,
    (5, 4): 8,
    (5, 6): 2,

    (6, 1): 10,
    (6, 2): 10,
    (6, 3): 10,
    (6, 4): 2,
    (6, 5): 8
}


# Create optimization model
model = gp.Model("Asymmetric_TSP")

# Create decision variables
x = model.addVars(
    cost.keys(),
    lb=0,
    ub=1,
    vtype=GRB.CONTINUOUS,
    name="x"
)

# Set objective function
model.setObjective(
    gp.quicksum(cost[i,j] * x[i,j] for i, j in cost),
    GRB.MINIMIZE
)

# Add constraints
for i in cities:
    model.addConstr(
        gp.quicksum(x[i,j] for j in cities if j != i) == 1,
        name=f"out_degree_{i}"
    )
    model.addConstr(
        gp.quicksum(x[j,i] for j in cities if j != i) == 1,
        name=f"in_degree_{i}"
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