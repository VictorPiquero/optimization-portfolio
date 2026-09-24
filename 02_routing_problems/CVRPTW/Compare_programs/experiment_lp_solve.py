from read_instance import read_solomon_instance



def write_dat(filename, n, k, Q, M, nodes, customers,
              cost, demand, earliest_time,
              latest_time, service_time):

    with open(filename, "w") as file:

        file.write("data;\n\n")

        # Parámetros simples
        file.write(f"param n := {n};\n")
        file.write(f"param k := {k};\n")
        file.write(f"param Q := {Q};\n")
        file.write(f"param M := {M};\n\n")

        # Demand
        file.write("param demand :=\n")
        for i in customers:
            file.write(f"{i} {demand[i]}\n")
        file.write(";\n\n")

        # Earliest time
        file.write("param earliest_time :=\n")
        for i in customers:
            file.write(f"{i} {earliest_time[i]}\n")
        file.write(";\n\n")

        # Latest time
        file.write("param latest_time :=\n")
        for i in nodes:
            file.write(f"{i} {latest_time[i]}\n")
        file.write(";\n\n")

        # Service time
        file.write("param service_time :=\n")
        for i in nodes:
            file.write(f"{i} {service_time[i]}\n")
        file.write(";\n\n")

        # Cost
        file.write("param cost :=\n")
        for i in nodes:
            for j in nodes:
                if i != j:
                    file.write(f"{i} {j} {cost[i,j]}\n")
        file.write(";\n\n")

        file.write("end;\n")



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
) = read_solomon_instance("02_routing_problems\\CVRPTW\\Compare_programs\\instances\\C1_6_1.TXT")

n = 100
k = 100

nodes = list(range(n + 1))
customers = list(range(1, n + 1))

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
    (i, j): all_cost[i, j]
    for i in nodes
    for j in nodes
    if i != j
}

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

write_dat(
    "02_routing_problems\\CVRPTW\\Compare_programs\\aux_temp.dat",
    n,
    k,
    Q,
    M,
    nodes,
    customers,
    cost,
    demand,
    earliest_time,
    latest_time,
    service_time
)
