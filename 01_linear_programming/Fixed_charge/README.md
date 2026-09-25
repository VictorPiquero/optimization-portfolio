# Fixed-Charge Problem

## Problem Description

Companies often face decisions that involve both **fixed costs** and **variable operating costs**.  
In these situations, a fixed cost must be paid before an activity can take place, while the variable cost depends on the level of activity.

**Sitka Manufacturing** is planning to build at least one new production plant. Three possible locations are being considered:

- Baytown, TX
- Lake Charles, LA
- Mobile, AL

Each plant has a different annual fixed cost, variable production cost, and annual production capacity.

Once the plants are built, the company wants to have enough capacity to produce at least **38,000 units per year**.

The objective is to determine:

- Which plants should be built.
- How many units should be produced at each plant.

while minimizing the **total annual cost**.

---

## Data

| Site | Annual Fixed Cost | Variable Cost per Unit | Annual Capacity |
|---|---:|---:|---:|
| Baytown, TX | $340,000 | $32 | 21,000 |
| Lake Charles, LA | $270,000 | $33 | 20,000 |
| Mobile, AL | $290,000 | $30 | 19,000 |

Minimum required production:


38,000 units/year


---

## Mathematical Model

The problem was formulated as a **Mixed-Integer Linear Programming (MILP)** model.

The model includes:

- Binary decision variables to determine which plants are built.
- Production variables representing the number of units produced at each plant.
- Fixed and variable production costs.
- A minimum production requirement.
- Capacity constraints linking plant construction and production decisions.

The complete mathematical formulation is shown below:

<p align="center">
  <img src="mat_model.png" width="750">
</p>

The constraint


y_i <= C_i x_i


links the plant-opening and production decisions. If a plant is not built (\(x_i=0\)), its production is forced to zero.

## Implementation

The model was implemented using **Microsoft Excel Solver**.

The spreadsheet contains:

- Input data for each candidate plant.
- Binary decision variables representing whether each plant is built.
- Production decision variables for each plant.
- Fixed and variable cost calculations.
- Capacity constraints.
- Minimum production requirement.
- Total annual cost calculation.

Excel Solver is configured to **minimize the total annual cost** while satisfying all production and capacity constraints.

---

## Optimization Model

This problem is a **Mixed-Integer Linear Programming (MILP)** problem because it combines:

- **Binary variables** for plant-opening decisions.
- **Continuous variables** for production quantities.
- A linear objective function.
- Linear constraints.

The capacity constraint

y_i <= C_i x_i

acts as a **linking constraint** between the strategic decision of opening a plant and the operational decision of producing at that plant.

---

## Files

- `Fixed_charge.xlsx` — Excel Solver implementation of the optimization model.
- `README.md` — Problem description and mathematical formulation.

---

## Tools

- Microsoft Excel
- Excel Solver