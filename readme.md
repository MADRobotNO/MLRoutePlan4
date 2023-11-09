# Route generator

## Description:
- Automatically generate route for a car
- Route length is 999km
- Route contains charging stations that are always in range of fully charged car (car_range > distance_to_next_charger):

  - Minimum distance between chargers is 5km
  - Maximum distance between chargers is car range - 10km
- ANN only used on charging spots
- Validating on every charging spot

## NEAT Configuration
- NEAT input:
  - Distance left
  - Current batter charge level
  - Distance to next charger
  - (Battery needed to reach next charger)
  - Time used
  - (Current speed)


- NEAT output:
  - Should charge
  - Charge to level
  - (Speed for next part)


- Fitness function:
  - factor = 0.0002
  - 1 - (time used * factor) - (battery level * factor)


- Number of generations : 100
- Population size: 20