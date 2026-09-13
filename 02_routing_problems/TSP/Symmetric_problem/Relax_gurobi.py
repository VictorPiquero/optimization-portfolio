# Import libraries
import gurobipy as gp
from gurobipy import GRB

# Define data

cities = [1, 2, 3, 4, 5, 6] # range(1, 7)

distance = {
    (2, 1): 2,
    (3, 1): 2,
    (4, 1): 10,
    (5, 1): 10,
    (6, 1): 10,
    (3, 2): 2,
    (4, 2): 10,
    (5, 2): 10,
    (6, 2): 10,
    (4, 3): 10,
    (5, 3): 10,
    (6, 3): 10,
    (5, 4): 2,
    (6, 4): 2,
    (6, 5): 2
}

# Create optimization model
model = gp.Model("TSP")

# Create decision variables
x = model.addVars(distance.keys(), vtype=GRB.BINARY, name="x")

# Set objective function
model.setObjective(
    gp.quicksum(distance[i,j] * x[i,j] for i, j in distance),
    GRB.MINIMIZE
)

# Add constraints
for i in cities:
    model.addConstr(
        gp.quicksum(x[i,j] for j in cities if j < i) +
        gp.quicksum(x[k,i] for k in cities if i < k) == 2,
        name=f"degree_{i}"
    )

# Solve model
model.optimize()

# Print results
if model.status == GRB.OPTIMAL:
    print("Optimal solution found")
    print(f"Optimal distance cost: {model.objVal}")

    for i, j in distance:
        if x[i, j].X > 0.5:
            print(f"Edge between city {i} and city {j}")

