## Mathematical formulation

![Mathematical formulation](mat_model.jpg)

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