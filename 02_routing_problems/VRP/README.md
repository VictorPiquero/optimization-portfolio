# Vehicle Routing Problem (VRP)

## Overview

The **Vehicle Routing Problem (VRP)** is a fundamental combinatorial optimization problem in transportation and logistics.

The objective is to determine a set of minimum-cost routes for a fleet of vehicles that serve a set of customers from a common depot. Each customer must be visited exactly once, and every route must start and end at the depot.

The VRP can be viewed as an extension of the **Traveling Salesman Problem (TSP)**. While the TSP searches for a single tour visiting all nodes, the VRP allows multiple routes associated with a fleet of vehicles.

In this project, the VRP is implemented using:

- **lp_solve** with GNU MathProg.
- **Gurobi Optimizer** with the Python API.

The purpose of this implementation is to understand the transition from the TSP to vehicle routing models before introducing additional constraints in the **Capacitated Vehicle Routing Problem (CVRP)** and the **Capacitated Vehicle Routing Problem with Time Windows (CVRPTW)**.

---

## Mathematical Formulation

The mathematical formulation used in this project is shown below.

<p align="center">
  <img src="mat_model.jpg" width="750" alt="VRP Mathematical Formulation">
</p>

---

## Linear Relaxation

Before solving the complete integer model, the linear relaxation is also considered.

This allows the behavior of the LP relaxation to be studied before enforcing integrality.

The comparison between the relaxed and integer formulations is useful for understanding the role of binary decision variables in routing problems.

---

## Example Instance

A small illustrative instance is used to test the formulation.

The instance consists of:

- **1 depot**: node 0.
- **6 customers**: nodes 1 to 6.
- **2 vehicles**.

The cost matrix is:

| From / To | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| **0** | - | 3 | 4 | 5 | 3 | 4 | 5 |
| **1** | 3 | - | 2 | 3 | 9 | 9 | 9 |
| **2** | 4 | 2 | - | 2 | 9 | 9 | 9 |
| **3** | 5 | 3 | 2 | - | 9 | 9 | 9 |
| **4** | 3 | 9 | 9 | 9 | - | 2 | 3 |
| **5** | 4 | 9 | 9 | 9 | 2 | - | 2 |
| **6** | 5 | 9 | 9 | 9 | 3 | 2 | - |

---

## Implementation

The same mathematical model is implemented using two optimization environments.

### lp_solve

The lp_solve implementation uses the **XLI_MathProg** interface and GNU MathProg syntax.

Two models are provided:

- `Relax_lpsolve.mod`: linear relaxation of the VRP.
- `Subtours_lpsolve.mod`: integer formulation including manually added subtour elimination constraints.

### Gurobi

The Gurobi implementation uses the **gurobipy** Python API.

Two equivalent implementations are provided:

- `Relax_gurobi.py`: linear relaxation of the VRP.
- `Subtours_gurobi.py`: integer formulation including manually added subtour elimination constraints.

Using the same instance in both optimization environments allows the formulations and results to be compared directly.

---

## Subtour Elimination

The depot and customer degree constraints alone do not guarantee that all customers belong to routes connected to the depot.

For example, the model may generate valid routes connected to the depot together with cycles involving only customers. These disconnected cycles are known as **subtours**.

For a subset of customers \(S\), a subtour elimination constraint can be expressed as:

\[
\sum_{\substack{i,j\in S\\i\neq j}} x_{ij} \leq |S|-1
\]

In the example considered in this project, subtours are identified after solving the initial model and the corresponding constraints are manually added.

This procedure illustrates the principle of iterative subtour elimination:

1. Solve the model.
2. Identify disconnected subtours.
3. Add the corresponding subtour elimination constraints.
4. Solve the model again.
5. Repeat until all customer routes are connected to the depot.

For larger instances, subtour detection and constraint generation should be automated.

---

## Repository Structure

```text
VRP/
│
├── mat_model.jpg
├── README.md
├── Relax_gurobi.py
├── Relax_lpsolve.mod
├── Subtours_gurobi.py
└── Subtours_lpsolve.mod
```

### Files

- `mat_model.jpg` — Mathematical formulation of the VRP.
- `Relax_gurobi.py` — Linear relaxation implemented with Gurobi.
- `Relax_lpsolve.mod` — Linear relaxation implemented with lp_solve/XLI_MathProg.
- `Subtours_gurobi.py` — Integer VRP with subtour elimination constraints implemented with Gurobi.
- `Subtours_lpsolve.mod` — Integer VRP with subtour elimination constraints implemented with lp_solve/XLI_MathProg.

---

## Learning Objectives

The objectives of this implementation are to:

- Understand the transition from the TSP to the VRP.
- Model multiple routes originating from a common depot.
- Understand depot and customer degree constraints.
- Identify disconnected subtours.
- Understand and apply subtour elimination constraints.
- Compare the LP relaxation with the integer formulation.
- Implement the same mathematical model using lp_solve and Gurobi.
- Establish the mathematical foundations required for the CVRP and CVRPTW.

---

## Technologies

- **Python**
- **Gurobi Optimizer**
- **lp_solve**
- **GNU MathProg**