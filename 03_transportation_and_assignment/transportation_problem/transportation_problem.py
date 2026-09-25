# Import libraries
import gurobipy as gp
from gurobipy import GRB

# Define data

mines = ["Mine1", "Mine2", "Mine3"]
transport = ["Type1", "Type2", "Type3", "Type4"]

cost = {
    ("Mine1", "Type1"): 2,
    ("Mine1", "Type2"): 2,
    ("Mine1", "Type3"): 2,
    ("Mine1", "Type4"): 1,
    ("Mine2", "Type1"): 10,
    ("Mine2", "Type2"): 8,
    ("Mine2", "Type3"): 5,
    ("Mine2", "Type4"): 4,
    ("Mine3", "Type1"): 7,
    ("Mine3", "Type2"): 6,
    ("Mine3", "Type3"): 6,
    ("Mine3", "Type4"): 8
}

production = {
    "Mine1": 3,
    "Mine2": 7,
    "Mine3": 5
}

transport_capacity = {
    "Type1": 4,
    "Type2": 3,
    "Type3": 4,
    "Type4": 4
}

# Create optimization model
model = gp.Model("transportation_problem")

# Create decision variables
x = model.addVars(mines, transport, vtype=GRB.CONTINUOUS, name="x")

# Set objective function
model.setObjective(
    gp.quicksum(cost[i,j] * x[i,j] for i in mines for j in transport),
    GRB.MINIMIZE
)

# Add constraints
for i in mines:
    model.addConstr(
        gp.quicksum(x[i,j] for j in transport) == production[i],
        name=f"production_{i}"
    )

for j in transport:
    model.addConstr(
        gp.quicksum(x[i,j] for i in mines) <= transport_capacity[j],
        name=f"transport_capacity_{j}"
    )


# Solve model
model.optimize()

# Print results
if model.status == GRB.OPTIMAL:
    print("Optimal solution found")
    print(f"Optimal transportation cost: {model.objVal}")

    for i in mines:
        for j in transport:
            print(f"{i,j}: {x[i,j].X}")
        

    for constr in model.getConstrs():
        print(f"{constr.ConstrName}: Slack = {constr.Slack}")

else:
    print("No optimal solution found")
