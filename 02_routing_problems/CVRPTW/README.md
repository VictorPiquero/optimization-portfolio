# Capacitated Vehicle Routing Problem with Time Windows (CVRPTW)

The **Capacitated Vehicle Routing Problem with Time Windows (CVRPTW)** is an extension of the Vehicle Routing Problem in which vehicles have limited capacity and each customer must be visited within a specified time window.

The objective is to determine a set of vehicle routes that serve all customers while satisfying vehicle capacity and time-window constraints and minimizing the total routing cost.

This section explores the CVRPTW through two different approaches: a basic implementation of the problem and an experimental comparison between optimization solvers.

---

## Repository Structure

### Basic Problem

The [`Basic_problem`](./Basic_problem) folder introduces the CVRPTW and its mathematical formulation.

It contains a basic implementation used to understand the main components of the problem, including:

- Vehicle routing decisions
- Vehicle capacity constraints
- Customer demands
- Time windows
- Service times
- Route continuity constraints

### Solver Comparison

The [`Compare_programs`](./Compare_programs) folder focuses on the computational performance of different optimization tools.

The same CVRPTW formulation is implemented using **Gurobi** and **lp_solve** and tested on instances of increasing size.

The comparison analyzes:

- Computational time
- Objective values
- Solver status
- Scalability as the number of customers increases

The experiments range from **10 to 500 customers**, allowing the differences between both solvers to become visible as the problem size increases.

---

## Tools

- Python
- Gurobi Optimizer
- lp_solve

---

## Concepts Covered

- Vehicle Routing Problem (VRP)
- Capacitated Vehicle Routing Problem (CVRP)
- Time Windows
- Mixed-Integer Linear Programming (MILP)
- Routing constraints
- Capacity constraints
- Solver performance comparison
- Computational experimentation