# Traveling Salesman Problem (TSP)

## Overview

The Traveling Salesman Problem (TSP) is one of the most fundamental and extensively studied problems in combinatorial optimization and operations research.

The objective is to determine the minimum-cost tour that visits every city exactly once and returns to the starting city. Despite its simple definition, the TSP is an NP-hard problem and serves as the foundation for many routing and logistics optimization problems.

In this project, the TSP is implemented using two optimization solvers:

- **lp_solve** (GNU MathProg)
- **Gurobi** (Python API)

The goal is to understand the mathematical formulation of the problem before extending it to more complex routing problems such as the Vehicle Routing Problem (VRP), the Capacitated Vehicle Routing Problem (CVRP), and the Capacitated Vehicle Routing Problem with Time Windows (CVRPTW).

---

## Problem Variants

This project includes two different formulations of the Traveling Salesman Problem.

### Symmetric Traveling Salesman Problem (STSP)

In the symmetric version, the travel cost between two cities is identical in both directions.

\[
c_{ij} = c_{ji}
\]

The transportation network is represented as an **undirected graph**, meaning that each connection between two cities is modeled using a single decision variable.

This formulation requires fewer variables and is commonly used when travel costs represent distances.

---

### Asymmetric Traveling Salesman Problem (ATSP)

In the asymmetric version, the travel cost depends on the travel direction.

\[
c_{ij} \neq c_{ji}
\]

The transportation network is represented as a **directed graph**, requiring one decision variable for every possible direction between two cities.

This formulation models more realistic situations such as:

- One-way streets
- Traffic conditions
- Different travel times
- Wind or slope effects
- Transportation costs depending on direction

---

## Mathematical Model

Both formulations share the same optimization objective:

- Minimize the total travel cost.
- Visit every city exactly once.
- Return to the starting city.
- Eliminate subtours to obtain a single Hamiltonian cycle.

The main difference between both formulations lies in the representation of the graph and the definition of the decision variables.

---

## Repository Structure

```
TSP/
│
├── README.md
│
├── symmetric_tsp/
│   ├── README.md
│   ├── lp_solve/
│   └── gurobi/
│
└── asymmetric_tsp/
    ├── README.md
    ├── lp_solve/
    └── gurobi/
```

Each implementation contains:

- Mathematical formulation
- Optimization model
- Example instances
- Solver implementation
- Results and discussion

---

## Learning Objectives

This project aims to:

- Understand graph-based optimization problems.
- Learn mathematical modeling techniques.
- Compare symmetric and asymmetric routing formulations.
- Implement optimization models using different solvers.
- Build the theoretical foundations required for the Vehicle Routing Problem (VRP) and its extensions.

---

## Technologies

- Python
- Gurobi Optimizer
- lp_solve
- GNU MathProg

---