# CVRPTW Solver Comparison: Gurobi vs. lp_solve

## Overview

This project compares the performance of **Gurobi** and **lp_solve** when solving the Capacitated Vehicle Routing Problem with Time Windows (CVRPTW).

The same mathematical formulation is implemented using both optimization tools and tested on problem instances of increasing size.

The objective of this experiment is to analyze how both solvers behave when solving the same MILP formulation, with particular attention to **computational time, solution quality, and solver status**.

---

## Problem Instances

The experiments were performed using CVRPTW instances with different numbers of customers:

- 10 customers
- 15 customers
- 20 customers
- 25 customers
- 50 customers
- 100 customers
- 200 customers
- 300 customers
- 400 customers
- 500 customers

For each instance, two different fleet sizes were considered.

Starting from a reference fleet size \(K_{ref}\), the available number of vehicles was increased by approximately:

- **+20%**
- **+50%**

This makes it possible to observe the behavior of the solvers under different fleet configurations.

---

## Experimental Setup

Both implementations solve the same CVRPTW formulation.

A maximum runtime of **1800 seconds (30 minutes)** was established for lp_solve.

The following information was collected:

| Metric | Description |
|---|---|
| Customers | Number of customers in the instance |
| \(K_{ref}\) | Reference fleet size |
| Fleet factor | Increase applied to the reference fleet |
| Vehicles | Number of vehicles available |
| Runtime | Computational time required by the solver |
| Objective | Best objective value obtained |
| Status | Final solver status |

---

## Results

| Customers | K_ref | Fleet factor | Vehicles | Gurobi (s) | Gurobi objective | Gurobi status | lp_solve (s) | lp_solve objective | lp_solve status |
|---:|---:|:---:|---:|---:|---:|:---:|---:|---:|:---:|
| 10 | 4 | +20% | 5 | 0.016 | 1221.806 | Optimal | 0.916 | 1221.806 | Optimal |
| 10 | 4 | +50% | 6 | 0.002 | 1326.216 | Optimal | 0.448 | 1326.216 | Optimal |
| 15 | 5 | +20% | 6 | 0.006 | 1625.072 | Optimal | 50.175 | 1625.072 | Optimal |
| 15 | 5 | +50% | 8 | 0.006 | 1755.131 | Optimal | 3.401 | 1755.131 | Optimal |
| 20 | 6 | +20% | 8 | 0.009 | 1964.603 | Optimal | 1800.01 | 1964.603 | Suboptimal |
| 20 | 6 | +50% | 9 | 0.011 | 2027.488 | Optimal | 205.001 | 2027.488 | Optimal |
| 25 | 7 | +20% | 9 | 0.063 | 2240.636 | Optimal | 1800.01 | -- | Timeout |
| 25 | 7 | +50% | 11 | 0.015 | 2348.628 | Optimal | 1800.00 | 2393.215 | Suboptimal |
| 50 | 10 | +20% | 12 | 0.077 | 3417.764 | Optimal | 1800.01 | -- | Timeout |
| 50 | 10 | +50% | 15 | 0.058 | 3478.188 | Optimal | 1800.00 | -- | Timeout |
| 100 | 17 | +20% | 21 | 0.219 | 5530.369 | Optimal | 1800.01 | -- | Timeout |
| 100 | 17 | +50% | 26 | 0.210 | 5702.862 | Optimal | 1800.01 | -- | Timeout |
| 200 | 31 | +20% | 38 | 1.199 | 9402.125 | Optimal | 1800.03 | -- | Timeout |
| 200 | 31 | +50% | 47 | 0.978 | 9883.168 | Optimal | 1800.03 | -- | Timeout |
| 300 | 38 | +20% | 46 | 5.219 | 11359.64 | Optimal | 1800.06 | -- | Timeout |
| 300 | 38 | +50% | 57 | 2.929 | 11853.93 | Optimal | 1800.08 | -- | Timeout |
| 400 | 49 | +20% | 59 | 9.040 | 13136.12 | Optimal | 1800.04 | -- | Timeout |
| 400 | 49 | +50% | 74 | 6.258 | 13927.31 | Optimal | 1800.03 | -- | Timeout |
| 500 | 56 | +20% | 68 | 17.916 | 14161.83 | Optimal | 1800.28 | -- | Timeout |
| 500 | 56 | +50% | 84 | 14.986 | 15108.20 | Optimal | 1800.14 | -- | Timeout |

> **Note:** `--` indicates that lp_solve did not report a feasible solution before reaching the time limit. `Timeout` indicates that the 1800-second time limit was reached without a reported feasible solution and does not imply that the instance is infeasible.

---

## Analysis

The results show a clear difference in computational performance between Gurobi and lp_solve as the size of the CVRPTW instances increases.

For the smallest instances, both solvers are able to obtain the same optimal solutions. With 10 customers, lp_solve solves both fleet configurations in less than one second, although Gurobi is already faster.

At 15 customers, the difference becomes more noticeable. Gurobi solves both instances in approximately 0.006 seconds, while lp_solve requires 3.401 seconds for the +50% fleet configuration and 50.175 seconds for the +20% configuration.

The 20-customer instances represent a significant change in computational difficulty for lp_solve. With the +50% fleet configuration, lp_solve still proves optimality, but requires 205.001 seconds compared with 0.011 seconds for Gurobi. With the +20% configuration, lp_solve reaches the 1800-second time limit without proving optimality, although the best solution found has the same objective value as the optimal solution obtained by Gurobi.

From 25 customers onwards, the difference becomes even more pronounced. lp_solve reaches the 1800-second time limit in every experiment, while Gurobi continues to solve all tested instances to optimality.

Even for the largest experiments with 500 customers, Gurobi obtains optimal solutions in approximately 15–18 seconds.

### Gurobi

Gurobi obtained an **optimal solution in every experiment**.

For the smallest instances, the required computational time was below one second. As the number of customers increased, runtime also increased, but all tested instances were still solved within a relatively short period.

For the largest instance with **500 customers**, Gurobi required approximately:

- **17.9 seconds** with the +20% fleet configuration.
- **15.0 seconds** with the +50% fleet configuration.

### lp_solve

lp_solve encountered considerably greater difficulty with the same formulation.

Of the 14 experiments, only the 25-customer instance with the +50% fleet configuration produced a feasible solution before the experiment ended. The reported objective value was:


2393.215


compared with Gurobi's optimal value of:


2348.628


For the remaining experiments, lp_solve reached the **1800-second time limit** without reporting a feasible solution.

---

## Conclusions

The experiments show that both implementations are consistent for the small instances where optimality can be verified by both solvers, as they obtain the same objective values.

However, their computational performance differs substantially as the problem size increases.

lp_solve performs adequately for the smallest instances, but its computational time grows rapidly. Difficulties become evident at around 20 customers, and from 25 customers onwards the solver reaches the 30-minute time limit in all tested configurations.

Gurobi shows much better performance for this formulation and experimental setup. It solves every tested instance to optimality, including the 500-customer cases, in less than 20 seconds.

These results illustrate how the choice of solver can have a major impact when solving large MILP models, even when the underlying mathematical formulation is the same.

---

## Tools

- Python
- Gurobi Optimizer
- lp_solve