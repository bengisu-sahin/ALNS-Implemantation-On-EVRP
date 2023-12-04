
import copy
from AlnsOperators.Operators import StationOperator
from DataObjects.ChargeStation import ChargeStation
import random

#CHARGE STATION REMOVAL OPERATORS

class randomStationRemovalOperator(StationOperator):
    def __init__(self):
        super().__init__()

    def removeStation(self,solution):
        Q = self.stationToBeRemoved(solution)
        charge_stations=solution.getAllStations()
        stations_to_remove = random.sample(charge_stations, int(Q))
        for route in solution.routes:
                for station in stations_to_remove:
                    if station in route.route:
                        route.remove_customer_from_route(station)
        return solution.routes
    
class  worstChargeUsageStationRemovalOperator(StationOperator):
    def __init__(self):
        super().__init__()

    def getChargeRemaining(self,station,selectedRoute):
        # Find the index of the station in the selectedRoute
        station_index = selectedRoute.route.index(station)

        # Copy elements from the beginning of selectedRoute until the station
        newRoute = copy.copy(selectedRoute)
        newRoute.route = selectedRoute.route[:station_index]
        return newRoute.calculate_remaining_tank_capacity()

    def removeStation(self,solution):
        charge_dict = {}
        Q = self.stationToBeRemoved(solution)
        for route_index, route in enumerate(solution.routes):
            for item in route.route:
                if isinstance(item, ChargeStation):
                # Get the current charge remaining for the ChargeStation
                    current_charge = self.getChargeRemaining(item, route)
                    
                    # Check if the ChargeStation ID is already in charge_dict
                    if item.id in charge_dict:
                        # Update the value with the maximum of the current and existing values
                        charge_dict[item][0] = max(charge_dict[item.id][0], current_charge)
                    else:
                        # If not present, add the ChargeStation ID with its current charge and route index
                        charge_dict[item] = [current_charge, route_index]

        # Sort the stations by charge remaining in descending order
        sorted_stations = sorted(charge_dict.items(), key=lambda x: x[1][0], reverse=True)

        # Take the top Q stations with the highest charge remaining
        stations_to_remove = sorted_stations[:int(Q)]

        # Remove the selected stations from the routes
        for charge_station_id, (charge_remaining, route_index) in stations_to_remove:
            solution.routes[route_index].remove_charge_station_from_route(charge_station_id)
            
        return solution.routes

#power required removal will be implemented
class worstStationRemovalOperator(StationOperator):
    def __init__(self):
        super().__init__()


# CHARGE STATION INSERTION OPERATORS        