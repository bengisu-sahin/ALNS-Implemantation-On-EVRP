import copy
from AlnsOperators.Operators import StationInsertionOperator, StationRemovalOperator

from DataObjects.Customer import Customer
from DataObjects.ChargeStation import ChargeStation
from collections import defaultdict
import random

# CHARGE STATION REMOVAL OPERATORS


class randomStationRemovalOperator(StationRemovalOperator):
    def __init__(self, score=0.0):
        super().__init__()
        self.score = score

    def remove(self, solution):
        Q = self.stationToBeRemoved(solution)
        charge_stations = solution.getAllStations()
        stations_to_remove = random.sample(charge_stations, int(Q))
        for route in solution.routes:
            for station in stations_to_remove:
                if station in route.route:
                    route.remove_customer_from_route(station)
        solution.removeEmptyRoutes()
        return solution.routes


class worstChargeUsageStationRemovalOperator(StationRemovalOperator):
    def __init__(self, score=0.0):
        super().__init__()
        self.score = score

    def getChargeRemaining(self, station, selectedRoute):
        # Find the index of the station in the selectedRoute
        station_index = selectedRoute.route.index(station)

        # Copy elements from the beginning of selectedRoute until the station
        newRoute = copy.copy(selectedRoute)
        newRoute.route = selectedRoute.route[:station_index]
        return newRoute.calculate_remaining_tank_capacity()

    def remove(self, solution):
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
                        charge_dict[item][0] = max(
                            charge_dict[item.id][0], current_charge
                        )
                    else:
                        # If not present, add the ChargeStation ID with its current charge and route index
                        charge_dict[item] = [current_charge, route_index]

        # Sort the stations by charge remaining in descending order
        sorted_stations = sorted(
            charge_dict.items(), key=lambda x: x[1][0], reverse=True
        )

        # Take the top Q stations with the highest charge remaining
        stations_to_remove = sorted_stations[: int(Q)]

        # Remove the selected stations from the routes
        for charge_station_id, (charge_remaining, route_index) in stations_to_remove:
            solution.routes[route_index].remove_charge_station_from_route(
                charge_station_id
            )
        solution.removeEmptyRoutes()
        return solution.routes


class worstStationRemovalOperator(StationRemovalOperator):
    def __init__(self, score=0.0):
        super().__init__()
        self.score = score

    def remove(self, solution):
        Q = self.stationToBeRemoved(solution)
        stations_to_remove = {}
        for route_index, route in enumerate(solution.routes):
            if route.get_charge_stations() != []:
                for index, item in enumerate(route.route):
                    if isinstance(item, ChargeStation):
                        stations_to_remove[route_index] = {
                            "item": item,
                            "energy": route.calculate_energy_consumption(
                                route.route[index - 1], item
                            ),
                        }

        sorted_stations = sorted(
            stations_to_remove.items(), key=lambda x: x[1]["energy"], reverse=True
        )
        stations_to_remove = sorted_stations[: int(Q)]
        for route_index, station in stations_to_remove:
            solution.routes[route_index].remove_charge_station_from_route(
                station["item"]
            )
        return solution


# CHARGE STATION INSERTION OPERATORS
class bestStationInsertionOperator(StationInsertionOperator):
    def __init__(self, score=0.0):
        super().__init__()
        self.score = score

    def insert(self, solution):
        charge_stations = solution.getAllStationInProblemFile()
        min_distance = []
        for route in solution.routes:
            if (
                route.is_feasible_all() == True
            ):  # if the tank capacity constraint is not violated, no need to add a charge station
                continue
            else:  # if the tank capacity constraint is violated, add the best charge station to the route
                # if there is no charge station in the route
                added_customer = route.get_node_before_where_battery_is_negative()
                added_customer_index = route.route.index(added_customer) - 1
                if added_customer_index == 0:
                    added_customer_index = 1
                get_closest_station = sorted(
                    charge_stations,
                    key=lambda station: station.distance_to(added_customer),
                )
                to_be_added_station = copy.deepcopy(get_closest_station)
                x = to_be_added_station[0]
                y = charge_stations[0]
                if x.id == y.id:
                    added_customer_index = len(route.route) - 1
                    to_be_added_station = to_be_added_station[1:]

                """
                Burada şöyle düşündüm makalede " If no previous recharge station 
                exists in solution, then the insertion is done between depot 
                and customer." diye bir ifade vardı. Ancak hangi şarj istasyonunun depo ile müşteri arasına ekleneceği belirtilmemişti.
                Bu yüzden burada şarj istasyonlarının depoya olan uzaklıklarını hesaplayıp en yakın olanı seçtim. 
                """

                for index, charge_station in enumerate(to_be_added_station):
                    route.append_charge_station_at_certain_point(
                        to_be_added_station[index], added_customer_index
                    )
                    to_be_added_stationd = to_be_added_station[index]
                    if route.is_feasible_all() == True:
                        break
                    else:
                        route.remove_charge_station_from_route(to_be_added_stationd)

                """
                Seçim yapılıp eklendikten sonra ise feasible olup olmadığı kontrol ediliyor. Eğer feasible değilse eklenen şarj istasyonu siliniyor. " Both operators check for feasibility of solution 
                after the station insertion. If no station can be inserted feasibly, the algorithm returns to the previous feasible solution." ifadesi makalede geçiyor diye bu şekilde kontrol ettim.
                """
                if route.is_feasible_all() == True:
                    continue
                else:
                    #TODO: Costlarını alıp en iyi costa göre ekleme yapılacak şekilde düzenlenecek.
                    for index, item in enumerate(route.route): 
                        sorted_charge_stations = sorted(
                            charge_stations[1:],
                            key=lambda station: station.distance_to(route.route[index+1]),
                        )
                        
                        for charge_station in sorted_charge_stations:
                            route.append_charge_station_at_certain_point(
                                charge_station, index + 1
                            )
                            if route.is_feasible_all() == True:
                                break
                            else:
                                route.remove_charge_station_from_route(charge_station)
                        if route.is_feasible_all() == True:
                            break
                            

        solution.removeEmptyRoutes()
        return solution


class Compare_K_Insertion(StationInsertionOperator):
    def __init__(self, k, score=0.0):
        super().__init__()
        self.k = k
        self.score = score

    def insert(self, solution):
        charge_stations = solution.getAllStationInProblemFile()
        costs = []
        
        get_unfeasible_routes = solution.getUnfeasibleRoutes()
        for route in get_unfeasible_routes:
            if route.is_feasible_all() == False:
                for customer in route.route:
                    if isinstance(customer, Customer):
                        available_charge = route.calculate_remaining_tank_capacity(
                            customer
                        )
                        to_node=route.route[route.route.index(customer) + 1]
                        needed_charge = route.calculate_charge_required_between_nodes(
                            customer, to_node
                        )
                        if available_charge < needed_charge:
                            temp_route = copy.deepcopy(route)
                            get_closest_charge_station = sorted(
                                charge_stations, key=lambda x: customer.distance_to(x)
                            )
                            for charge_station in get_closest_charge_station:
                                temp_route.append_charge_station_at_certain_point(
                                    charge_station,
                                    route.route.index(customer)+1,
                                )
                                if temp_route.is_feasible_all() == True:
                                    costs.append(
                                        (
                                            copy.deepcopy(temp_route.calculate_obj_function()),
                                            copy.deepcopy(temp_route),
                                            solution.find_route_index_in_solution(route),
                                        )
                                    )
                                    temp_route.remove_charge_station_from_route(
                                        charge_station
                                    )
                                else:
                                    temp_route.remove_charge_station_from_route(
                                        charge_station
                                    )
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            
                            # route.append_charge_station_at_certain_point(
                            #     get_closest_charge_station[0],
                            #     route.route.index(customer) + 1,
                            # )
                            # if route.is_feasible_all() == False:
                            #     route.remove_charge_station_from_route(
                            #         get_closest_charge_station[0]
                            #     )
                            # else:
                            #     temp_route = copy.copy(route)
                            #     temp_route.route = route.route.copy()
                            #     costs.append(
                            #         (
                            #             temp_route.calculate_obj_function(),
                            #             temp_route,
                            #             route_index,
                            #         )
                            #     )
                            #     route.remove_charge_station_from_route(
                            #         get_closest_charge_station[0]
                            #     )
            
        k = self.k
        if len(costs) < k + 1:
            k = 0
            
        if(len(costs)==0):
            return solution
        
        tobeadded_route = costs[k][1]
        tobeadded_route_index = costs[k][2]
        solution.routes[tobeadded_route_index] = tobeadded_route
        solution.removeEmptyRoutes()

        return solution
