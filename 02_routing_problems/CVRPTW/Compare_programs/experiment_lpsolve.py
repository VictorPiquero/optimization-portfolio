import subprocess
import csv
import re
import math
from pathlib import Path

from read_instance import read_solomon_instance


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

INSTANCE = BASE_DIR / "instances" / "C1_6_1.TXT"
MODEL = BASE_DIR / "cvrptw.mod"
DATA = BASE_DIR / "temp.dat"

LPSOLVE = Path(r"C:\lp_solve\lp_solve.exe")
XLI = Path(r"C:\lp_solve\xli_MathProg.dll")

OUTPUT_FOLDER = BASE_DIR / "outputs"
OUTPUT_FOLDER.mkdir(exist_ok=True)

CSV_FILE = BASE_DIR / "results_lpsolve.csv"


# ============================================================
# EXPERIMENTS
# ============================================================

# Feasible reference fleet obtained in preliminary experiments
experiments = {
    25: 7,
    50: 10,
    100: 17,
    200: 31,
    300: 38,
    400: 49,
    500: 56,
}

TIME_LIMIT = 1800


# ============================================================
# WRITE .DAT FILE
# ============================================================

def write_dat(filename, n, k, Q, M, nodes, customers,
              cost, demand, earliest_time,
              latest_time, service_time):

    with open(filename, "w") as file:

        file.write("data;\n\n")

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
                    file.write(f"{i} {j} {cost[i, j]}\n")
        file.write(";\n\n")

        file.write("end;\n")


# ============================================================
# RUN LP_SOLVE
# ============================================================

def run_lpsolve(n, k):

    command = [
    str(LPSOLVE),
    "-timeout", str(TIME_LIMIT),
    "-time",
    "-S1",
    "-rxlidata", str(DATA),
    "-rxli", str(XLI),
    str(MODEL)
    ]

    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    output = result.stdout + result.stderr

    # --------------------------------------------------------
    # Save complete lp_solve output
    # --------------------------------------------------------

    txt_file = OUTPUT_FOLDER / f"n{n}_k{k}.txt"

    with open(txt_file, "w") as file:
        file.write(output)

    # --------------------------------------------------------
    # Runtime
    # --------------------------------------------------------

    match = re.search(
        r"CPU Time for solving:\s*([\d.]+)s",
        output
    )

    if match:
        runtime = float(match.group(1))
    else:
        runtime = None

    # --------------------------------------------------------
    # Objective
    # --------------------------------------------------------

    match = re.search(
        r"Value of objective function:\s*([-\d.eE+]+)",
        output
    )

    if match:
        objective = float(match.group(1))
    else:
        objective = None

    # --------------------------------------------------------
    # Status
    # --------------------------------------------------------

    if "Suboptimal solution" in output:
        status = "Suboptimal"

    elif "Timeout" in output:
        status = "Timeout"

    elif objective is not None:
        status = "Optimal"

    else:
        status = "Unknown"

    return runtime, objective, status


# ============================================================
# READ INSTANCE
# ============================================================

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
) = read_solomon_instance(INSTANCE)


# ============================================================
# CSV
# ============================================================

fieldnames = [
    "customers",
    "k_ref",
    "fleet_factor",
    "vehicles",
    "runtime",
    "objective",
    "status"
]


# Create CSV and header only if it does not exist
if not CSV_FILE.exists():

    with open(CSV_FILE, "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
            delimiter=";"
        )

        writer.writeheader()


# ============================================================
# EXPERIMENT LOOP
# ============================================================

for n, k_ref in experiments.items():

    print()
    print("=" * 60)
    print(f"Customers: {n}")
    print("=" * 60)

    # --------------------------------------------------------
    # Select first n customers
    # --------------------------------------------------------

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

    # --------------------------------------------------------
    # Big-M
    # --------------------------------------------------------

    M_customers = max(
        latest_time[i]
        + service_time[i]
        + cost[i, j]
        - earliest_time[j]

        for i in customers
        for j in customers
        if i != j
    )

    M_depot = max(
        service_time[0]
        + cost[0, j]
        - earliest_time[j]

        for j in customers
    )

    M = max(0, M_customers, M_depot)

    # --------------------------------------------------------
    # +20% and +50% fleet
    # --------------------------------------------------------

    fleet_cases = [
        ("+20%", math.ceil(k_ref * 1.20)),
        ("+50%", math.ceil(k_ref * 1.50))
    ]

    for fleet_factor, k in fleet_cases:

        print()
        print(f"Running n={n}, k={k} ({fleet_factor})...")

        # ----------------------------------------------------
        # Generate temp.dat
        # ----------------------------------------------------

        write_dat(
            DATA,
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

        # ----------------------------------------------------
        # Run lp_solve
        # ----------------------------------------------------

        runtime, objective, status = run_lpsolve(n, k)

        # ----------------------------------------------------
        # Save result immediately
        # ----------------------------------------------------

        row = {
            "customers": n,
            "k_ref": k_ref,
            "fleet_factor": fleet_factor,
            "vehicles": k,
            "runtime": runtime,
            "objective": objective,
            "status": status
        }

        with open(CSV_FILE, "a", newline="") as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fieldnames,
                delimiter=";"
            )

            writer.writerow(row)

        # ----------------------------------------------------
        # Show only summary in terminal
        # ----------------------------------------------------

        print(
            f"n={n} | "
            f"k={k} | "
            f"{fleet_factor} | "
            f"runtime={runtime} s | "
            f"status={status} | "
            f"objective={objective}"
        )


print()
print("Experiments finished.")
print(f"Results: {CSV_FILE}")
print(f"Complete outputs: {OUTPUT_FOLDER}")