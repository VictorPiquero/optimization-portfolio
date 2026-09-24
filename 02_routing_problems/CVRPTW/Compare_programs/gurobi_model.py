import gurobipy as gp
from gurobipy import GRB


def solve_cvrptw(
    nodes,
    customers,
    k,
    Q,
    demand,
    earliest_time,
    latest_time,
    service_time,
    cost,
    M,
    time_limit=1800
):
    
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

    # Depot time window constraints
    for i in customers:
        model.addConstr(
            t[i] + service_time[i] + cost[i,0] <= latest_time[0] + M * (1 - x[i,0]),
            name=f"depot_latest_{i}"
        )

    # Maximum execution time
    model.Params.TimeLimit = time_limit

    # Solve
    model.optimize()


    # =========================
    # Results
    # =========================

    runtime = model.Runtime
    best_bound = model.ObjBound

    if model.SolCount > 0:

        objective = model.ObjVal
        gap = model.MIPGap * 100

        if model.Status == GRB.OPTIMAL:
            status = "Optimal"

        elif model.Status == GRB.TIME_LIMIT:
            status = "Time limit"

        else:
            status = f"Status {model.Status}"

    else:

        objective = None
        gap = None

        if model.Status == GRB.TIME_LIMIT:
            status = "Time limit - No solution"

        elif model.Status == GRB.INFEASIBLE:
            status = "Infeasible"

        else:
            status = f"Status {model.Status}"


    return {
        "runtime": runtime,
        "objective": objective,
        "best_bound": best_bound,
        "gap": gap,
        "status": status
    }