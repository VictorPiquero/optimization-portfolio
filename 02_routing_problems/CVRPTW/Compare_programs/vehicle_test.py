from read_instance import read_solomon_instance
from gurobi_model import solve_cvrptw
import csv
import math


fieldnames = [
    "customers",
    "capacity_lb",
    "vehicles",
    "solver",
    "runtime",
    "objective",
    "best_bound",
    "gap",
    "status"
]

with open("Results/results_test_vehicles.csv", "w", newline="") as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()


(
    all_nodes,
    all_customers,
    max_vehicles,
    Q,
    all_demand,
    all_earliest_time,
    all_latest_time,
    all_service_time,
    all_cost
) = read_solomon_instance("instances\\C1_6_1.TXT")


customer_sizes = [
    25,
    50,
    100,
    200,
    300,
    400,
    500
]


for n in customer_sizes:

    customers = all_customers[:n]
    nodes = [0] + customers

    demand = {
        i: all_demand[i]
        for i in customers
    }

    earliest_time = {
        i: all_earliest_time[i]
        for i in customers
    }

    latest_time = {
        i: all_latest_time[i]
        for i in nodes
    }

    service_time = {
        i: all_service_time[i]
        for i in nodes
    }

    cost = {
        (i,j): all_cost[i,j]
        for i in nodes
        for j in nodes
        if i != j
    }


    total_demand = sum(
    demand[i]
    for i in customers
    )

    capacity_lb = math.ceil(total_demand / Q)

    k_20 = math.ceil(capacity_lb * 1.20)
    k_50 = math.ceil(capacity_lb * 1.50)
    max_vehicles = len(customers)

    for k in range(capacity_lb, max_vehicles + 1):

        print(f"Solving CVRPTW with {n} customers and {k} vehicles...")

        M_customers = max(
            latest_time[i] + service_time[i] + cost[i,j] - earliest_time[j]
            for i in customers
            for j in customers
            if i != j
        )

        M_depot = max(
            service_time[0] + cost[0,j] - earliest_time[j]
            for j in customers
        )

        M = max(0, M_customers, M_depot)

        result = solve_cvrptw(
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
        )

        row = {
        "customers": n,
        "capacity_lb": capacity_lb,
        "vehicles": k,
        "solver": "Gurobi",
        "runtime": result["runtime"],
        "objective": result["objective"],
        "best_bound": result["best_bound"],
        "gap": result["gap"],
        "status": result["status"]
        }

        with open("Results/results_test_vehicles.csv", "a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writerow(row)