## Mathematical formulation

### Sets

Let \(P\) be the set of hot tub models.

\[
P = \{\text{Aqua-Spa}, \text{Hydro-Lux}\}
\]

### Decision variables

\[
x_i = \text{number of units of model } i \text{ to produce}, \quad i \in P
\]

### Parameters

| Parameter | Description |
|----------|-------------|
| \(p_i\) | Profit per unit of model \(i\) |
| \(h_i\) | Labor hours required to produce one unit of model \(i\) |
| \(t_i\) | Feet of tubing required to produce one unit of model \(i\) |
| \(H\) | Total labor hours available |
| \(T\) | Total feet of tubing available |
| \(B\) | Total number of pumps available |

### Objective function

The objective is to maximize the total profit:

\[
\max \sum_{i \in P} p_i x_i
\]

### Constraints

Labor capacity:

\[
\sum_{i \in P} h_i x_i \leq H
\]

Tubing capacity:

\[
\sum_{i \in P} t_i x_i \leq T
\]

Pump availability:

\[
\sum_{i \in P} x_i \leq B
\]

Variable domain:

\[
x_i \in \mathbb{Z}_{\geq 0}, \quad i \in P
\]

### Data

| Model | Profit | Labor hours | Tubing | Pumps |
|------|-------:|------------:|-------:|------:|
| Aqua-Spa | 350 | 9 | 12 | 1 |
| Hydro-Lux | 300 | 6 | 16 | 1 |

Available resources:

| Resource | Availability |
|----------|-------------:|
| Labor hours | 1566 |
| Tubing | 2880 |
| Pumps | 200 |


## Results

Optimal solution:

| Variable | Value |
|----------|------:|
| Aqua-Spa | 122 |
| Hydro-Lux | 78 |

Optimal profit:

$66100

Constraints slack:

| Constraint | Value |
|----------|------:|
| labor_capacity | 0.0 |
| tubing_capacity | 168.0 |
| pump_availability | 0.0 |

The analysis of the constraint slack shows that labor capacity and pump availability are binding constraints, as both have zero slack. This means that these resources are fully utilized and are the limiting factors in the production plan. In contrast, the tubing constraint has a slack of 168 feet, indicating that some tubing remains unused and is therefore not a limiting resource.