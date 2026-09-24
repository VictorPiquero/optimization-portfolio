import math

def read_solomon_instance(file_path):

    # Read file
    with open(file_path, "r") as file:
        lines = file.readlines()

    # --------------------------------------------------
    # Vehicle data
    # --------------------------------------------------

    vehicle_index = next(
        i for i, line in enumerate(lines)
        if line.strip() == "VEHICLE"
    )

    vehicle_data = lines[vehicle_index + 2].split()

    max_vehicles = int(vehicle_data[0])
    Q = int(vehicle_data[1])


    # --------------------------------------------------
    # Customer data
    # --------------------------------------------------

    customer_index = next(
        i for i, line in enumerate(lines)
        if line.strip() == "CUSTOMER"
    )

    data = []

    # Customer data starts 3 lines after "CUSTOMER"
    for line in lines[customer_index + 3:]:

        values = line.split()

        if len(values) >= 7:

            node = int(values[0])
            x = float(values[1])
            y = float(values[2])
            demand = int(values[3])
            earliest = float(values[4])
            latest = float(values[5])
            service = float(values[6])

            data.append(
                (node, x, y, demand, earliest, latest, service)
            )


    # --------------------------------------------------
    # Sets
    # --------------------------------------------------

    nodes = [row[0] for row in data]

    customers = [
        node for node in nodes
        if node != 0
    ]


    # --------------------------------------------------
    # Coordinates
    # --------------------------------------------------

    x_coord = {
        row[0]: row[1]
        for row in data
    }

    y_coord = {
        row[0]: row[2]
        for row in data
    }


    # --------------------------------------------------
    # Demand
    # --------------------------------------------------

    demand = {
        row[0]: row[3]
        for row in data
        if row[0] != 0
    }


    # --------------------------------------------------
    # Time windows
    # --------------------------------------------------

    earliest_time = {
        row[0]: row[4]
        for row in data
        if row[0] != 0
    }

    latest_time = {
    row[0]: row[5]
    for row in data
    }


    # --------------------------------------------------
    # Service times
    # --------------------------------------------------

    service_time = {
        row[0]: row[6]
        for row in data
    }


    # --------------------------------------------------
    # Travel costs / travel times
    # --------------------------------------------------

    cost = {}

    for i in nodes:
        for j in nodes:

            if i != j:

                cost[i, j] = math.sqrt(
                    (x_coord[i] - x_coord[j])**2
                    + (y_coord[i] - y_coord[j])**2
                )


    return (
        nodes,
        customers,
        max_vehicles,
        Q,
        demand,
        earliest_time,
        latest_time,
        service_time,
        cost
    )
