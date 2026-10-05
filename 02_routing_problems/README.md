# Routing Problems

This section of the portfolio focuses on **routing optimization problems**, one of the main areas of Operations Research with applications in logistics, transportation, and supply chain management.

The objective is to study how routing models evolve from simple formulations to more realistic problems by progressively introducing additional constraints such as multiple vehicles, vehicle capacities, customer demands, and time windows.

---

## Problem Progression

The routing problems are studied following a progressive approach:

**TSP → VRP → CVRP → CVRPTW**

Each problem extends the previous one by introducing new decisions and constraints.

| Problem | Description | Main Extension |
|---|---|---|
| TSP | Traveling Salesman Problem | Find the minimum-cost tour visiting all nodes |
| VRP | Vehicle Routing Problem | Introduces multiple vehicles and a depot |
| CVRP | Capacitated Vehicle Routing Problem | Adds vehicle capacities and customer demands |
| CVRPTW | Capacitated Vehicle Routing Problem with Time Windows | Adds service times and customer time windows |

---

## Repository Structure

### Traveling Salesman Problem (TSP)

The [`TSP`](./TSP) section introduces the fundamental routing problem in which a single route must visit every node exactly once and return to the starting point.

Both **symmetric and asymmetric** formulations are explored.

### Vehicle Routing Problem (VRP)

The [`VRP`](./VRP) section extends the TSP by introducing a **depot and multiple vehicles**.

It introduces the basic structure used in more advanced vehicle routing models.

### Capacitated Vehicle Routing Problem (CVRP)

The [`CVRP`](./CVRP) section incorporates **customer demands and vehicle capacity constraints**.

This introduces an important operational restriction commonly found in real logistics and distribution problems.

### Capacitated Vehicle Routing Problem with Time Windows (CVRPTW)

The [`CVRPTW`](./CVRPTW) section extends the CVRP by introducing **time windows and service times**.

In addition to the basic implementation, this section includes a computational comparison between **Gurobi and lp_solve** using instances of increasing size.

---

## Mathematical Optimization

The routing problems are formulated mainly as **Mixed-Integer Linear Programming (MILP)** models.

Throughout the different problems, concepts such as the following are progressively introduced:

- Binary routing variables
- Depot constraints
- Flow conservation
- Subtour elimination
- Multiple vehicles
- Customer demands
- Vehicle capacity
- Time windows
- Service times

---

## Tools

- Python
- Gurobi Optimizer
- lp_solve

---

## Concepts Covered

- Traveling Salesman Problem (TSP)
- Vehicle Routing Problem (VRP)
- Capacitated Vehicle Routing Problem (CVRP)
- Capacitated Vehicle Routing Problem with Time Windows (CVRPTW)
- Mixed-Integer Linear Programming (MILP)
- Network and routing optimization
- Subtour elimination
- Capacity constraints
- Time-window constraints
- Solver performance analysis