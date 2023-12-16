
import copy
from AlnsOperators.Operators import StationInsertionOperator, StationRemovalOperator

from DataObjects.Customer import Customer
from DataObjects.ChargeStation import ChargeStation
import random

#CHARGE STATION REMOVAL OPERATORS

class randomStationRemovalOperator(StationRemovalOperator):
    def __init__(self):
        super().__init__()

    def remove(self,solution):
        Q = self.stationToBeRemoved(solution)
        charge_stations=solution.getAllStations()
        stations_to_remove = random.sample(charge_stations, int(Q))
        for route in solution.routes:
                for station in stations_to_remove:
                    if station in route.route:
                        route.remove_customer_from_route(station)
        solution.removeEmptyRoutes()
        return solution.routes
    
class  worstChargeUsageStationRemovalOperator(StationRemovalOperator):
    def __init__(self):
        super().__init__()

    def getChargeRemaining(self,station,selectedRoute):
        # Find the index of the station in the selectedRoute
        station_index = selectedRoute.route.index(station)

        # Copy elements from the beginning of selectedRoute until the station
        newRoute = copy.copy(selectedRoute)
        newRoute.route = selectedRoute.route[:station_index]
        return newRoute.calculate_remaining_tank_capacity()

    def remove(self,solution):
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
        solution.removeEmptyRoutes()    
        return solution.routes

#TODO required removal will be implemented
class worstStationRemovalOperator(StationRemovalOperator):
    def __init__(self):
        super().__init__()


# CHARGE STATION INSERTION OPERATORS        
class bestStationInsertionOperator(StationInsertionOperator):
    def __init__(self):
        super().__init__()

    def insert(self,solution):
        charge_stations=solution.getAllStations()
        min_distance =[]
        for route in solution.routes: 
            if route.tank_capacity_constraint_violated==False: #if the tank capacity constraint is not violated, no need to add a charge station
                continue
            else: #if the tank capacity constraint is violated, add the best charge station to the route
                if route.number_of_charge_stations() == 0: #if there is no charge station in the route  
                    min_distance.append(charge_stations[0])
                    min_distance.append(route.get_first_customer().distance_to(charge_stations[0])) 
                    """
                    Burada şöyle düşündüm makalede " If no previous recharge station 
                    exists in solution, then the insertion is done between depot 
                    and customer." diye bir ifade vardı. Ancak hangi şarj istasyonunun depo ile müşteri arasına ekleneceği belirtilmemişti.
                    Bu yüzden burada şarj istasyonlarının depoya olan uzaklıklarını hesaplayıp en yakın olanı seçtim. 
                    """
                    for station in charge_stations[1:]: #find the closest charge station to the first customer of the route
                        distance = route.get_first_customer().distance_to(station)
                        if distance < min_distance[1]:
                            min_distance[1] = distance
                            min_distance[0] = station
                    route.append_charge_station_at_certain_point(min_distance[0],1)
                    """
                    Seçim yapılıp eklendikten sonra ise feasible olup olmadığı kontrol ediliyor. Eğer feasible değilse eklenen şarj istasyonu siliniyor. " Both operators check for feasibility of solution 
                    after the station insertion. If no station can be inserted feasibly, the algorithm returns to the previous feasible solution." ifadesi makalede geçiyor diye bu şekilde kontrol ettim.
                    """
                    if route.is_feasible_all() == True:
                        continue    
                    else:
                        route.remove_charge_station_from_route(min_distance[0])
                else: #if there is at least one charge station in the route
                    if route.tank_capacity_constraint_violated == True: #if the tank capacity constraint is violated, add the best charge station to the route 
                        for index, item in enumerate(route.route):
                            if route.calculate_remaining_tank_capacity(item)<0: #find the customer that violates the tank capacity constraint
                                #find the closest charge station to the violating customer
                                """
                                Burada şöyle düşündüm makalede bu if e giren kısım şu demek bu item a ulaşınca tank capacity constraint i bozuluyor. Eksiye düşüyor. Demekki benim item dan önceki yere şarj istasyonu eklemem gerekiyor. En yakın şarj istasyonunu bulup ekliyorum.
                                
                                """
                                min_distance.append(charge_stations[0]) 
                                min_distance.append(route.route[index-1].distance_to(charge_stations[0])) 
                                for station in charge_stations[1:]:
                                    distance = route.route[index-1].distance_to(station)
                                    if distance < min_distance[1]:
                                        min_distance[1] = distance
                                        min_distance[0] = station
                                route.append_charge_station_at_certain_point(min_distance[0],index) #add the closest charge station 
                                if route.is_feasible_all() == True: #check if the solution is feasible
                                    continue    
                                else: #if the solution is not feasible, remove the charge station
                                    route.remove_charge_station_from_route(min_distance[0])
        solution.removeEmptyRoutes()
        return solution
    
class Compare_K_Insertion(StationInsertionOperator):
    def __init__(self,k,score):
        super().__init__()
        self.k=k
        self.score=score
    def insert(self, solution):
        charge_stations = solution.getAllStationInProblemFile()
        costs=[]
        route_index=0
        for route in solution.routes:
            if(route.tank_capacity_constraint_violated()==True):
                for customer in route.route:
                    if isinstance(customer, Customer):
                        
                        available_charge=route.calculate_remaining_tank_capacity(customer)
                        needed_charge=route.calculate_charge_required_between_nodes(customer,route.route[route.route.index(customer)+1])
                        if(available_charge<needed_charge):
                            get_closest_charge_station=sorted(charge_stations,key=lambda x:customer.distance_to(x))   
                            route.append_charge_station_at_certain_point(get_closest_charge_station[0],route.route.index(customer)+1)
                            if(route.is_feasible_all()==False):
                                route.remove_charge_station_from_route(get_closest_charge_station[0])
                            else:
                                temp_route = copy.copy(route)
                                temp_route.route = route.route.copy()
                                costs.append((temp_route.calculate_obj_function(),temp_route,route_index))
                                route.remove_charge_station_from_route(get_closest_charge_station[0])
            route_index+=1
            
        tobeadded_route=costs[self.k][1]
        tobeadded_route_index=costs[self.k][2]
        solution.routes[tobeadded_route_index]=tobeadded_route
        solution.removeEmptyRoutes()
                
                
        return solution
    
        