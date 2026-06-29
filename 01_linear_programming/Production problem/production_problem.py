# Import libraries
import gurobipy as gp
from gurobipy import GRB

# Define data

products = ["Aqua-Spa", "Hydro-Lux"]

profit = {
    "Aqua-Spa": 350,
    "Hydro-Lux": 300
}

labor = {
    "Aqua-Spa": 9,
    "Hydro-Lux": 6
}

tubing = {
    "Aqua-Spa": 12,
    "Hydro-Lux": 16
}

available_labor = 1566
available_tubing = 2880
available_pumps = 200


# Create optimization model
model = gp.Model("production_problem")

# Create decision variables
x = model.addVars(products, vtype=GRB.INTEGER, name="x")

# Set objective function
model.setObjective(
    gp.quicksum(profit[i] * x[i] for i in products),
    GRB.MAXIMIZE
)

# Add constraints
model.addConstr(
    gp.quicksum(labor[i] * x[i] for i in products) <= available_labor,
    name="labor_capacity"
)

model.addConstr(
    gp.quicksum(tubing[i] * x[i] for i in products) <= available_tubing,
    name="tubing_capacity"
)

model.addConstr(
    gp.quicksum(x[i] for i in products) <= available_pumps,
    name="pump_availability"
)

# Solve model
model.optimize()

# Print results
if model.status == GRB.OPTIMAL:
    print("Optimal solution found")
    print(f"Optimal profit: {model.objVal}")

    for i in products:
        print(f"{i}: {x[i].X}")

    for constr in model.getConstrs():
        print(f"{constr.ConstrName}: Slack = {constr.Slack}")

else:
    print("No optimal solution found")



