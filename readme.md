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
  - Time used


- NEAT output:
  - Should charge
  - Charge to level


- Fitness function:
  - factor = 0.0002
  - stop factor = ~~0.02~~ 0.04
  - battery factor = 0.005
  - 1 - (time used * factor) - (battery level * battery factor) - (number of stops * stop_factor)


- Population size: 100 


## Refactors:
- Added multiple routes for each genome in training process
- Added battery factor (0.005) to fitness function
- Changed stop factor to 0.04