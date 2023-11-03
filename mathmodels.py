import math
from DataObjects.ChargeStation import ChargeStation


# Calculate the result of the equation
def calculateEstimatedEnginePower():
    #
    # Calculate the result of the equation
    #
    # Return the result
    return 0
    

def calculate_remaining_tank_capacity(route, config):
    elapsed_time = route[0].ready_time + route[0].service_time

    for i in range(1, len(route)):
        elapsed_time = elapsed_time + route[i - 1].distance_to(route[i]) / config.velocity

        if type(route[i]) is ChargeStation:
            missing_energy = config.tank_capacity - calculate_remaining_tank_capacity(route[i])
            route[i] = missing_energy * config.charging_rate

        waiting_time = max(route[i].ready_time - elapsed_time, 0)
        elapsed_time += waiting_time
        elapsed_time += route[i].service_time

    return elapsed_time


    

