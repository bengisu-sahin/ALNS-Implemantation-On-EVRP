
from DataObjects.Customer import Customer
from DataObjects.ChargeStation import ChargeStation

class Solution:
    
    def __init__(self,unserved_customers,served_customers, routes,problemFile ):
        self.unserved_customers = unserved_customers
        self.served_customers = served_customers
        self.routes = routes
        self.problemFile = problemFile
        self.iteration_list=[]
        self.total_distance_list=[]

    def setIterationList(self,iteration_list):
        self.iteration_list=iteration_list

    def setTotalDistanceList(self,total_distance_list):
        self.total_distance_list=total_distance_list
    
    def getNumberOfCustomers(self):
        totalCustomers=0
        for route in self.routes:
            for customer in route.route:
                if(type(customer) is Customer):
                    totalCustomers+=1
        return totalCustomers
    
    def getAllCustomers(self):
        allCustomers=[]
        for route in self.routes:
            for customer in route.route:
                if(type(customer) is Customer):
                    allCustomers.append(customer)
        return allCustomers
    
    def getNumberOfStation(self):
        numOfStations = 0
        for route in self.routes:
            for item in route.route:
                if(type(item) is ChargeStation):
                    numOfStations+=1
        return numOfStations
    def remove_w_id_served(self, customer):
        for item in self.served_customers:
            if item.id == customer.id:
                self.served_customers.remove(item)
    
    def remove_w_id_unserved(self, customer):
        for item in self.unserved_customers:
            if item.id == customer.id:
                self.unserved_customers.remove(item)
                
    def getAllStations(self):
        allStations=[]
        for route in self.routes:
            for item in route.route:
                if type(item) is ChargeStation and item not in allStations:
                    allStations.append(item)
        return allStations
    
    def getAllStationsWithRouteIndexAndStationIndex(self):
        allStations=[]
        for route in self.routes:
            for station in route.route:
                if type(station) is ChargeStation and station not in allStations:
                    allStations.append([route.route.index(station),self.routes.index(route),station])
        return allStations

    def isAllRoutesFeasible(self):
        for route in self.routes:
            if route.is_feasible_all() == False:
                return False
        return True
    def getnumberofFeasibleAndUnfeasibleRoutes(self):
        feasible=0
        unfeasible=0
        for route in self.routes:
            if route.is_feasible_all() == False:
                unfeasible+=1
            else:
                feasible+=1
        return feasible,unfeasible
    def get_Total_Objective_Function_Value(self):
        total=0
        for route in self.routes:
            total += route.calculate_obj_function()
        return total
    def getUnfeasibleRoutes(self):
        unfeasibleRoutes=[]
        for route in self.routes:
            if route.is_feasible_all() == False:
                unfeasibleRoutes.append(route)
        return unfeasibleRoutes
    def find_route_index_in_solution(self,route):
        for i in range(len(self.routes)):
            if self.routes[i] == route:
                return i
        return -1
    
    def getUnservedCustomers(self):
        return self.unserved_customers

    def getAllStationInProblemFile(self):
        return self.problemFile.charging_stations
    
    def getAllCustomersInProblemFile(self):
        return self.problemFile.customers
    
    def getTotalDistance(self):
        totalDistance=0
        for route in self.routes:
            totalDistance+=route.calculate_total_distance()
        return totalDistance
    
    def getUnfeasibleRoutes_indexes(self):
        unfeasibleRoutes=[]
        for i in range(len(self.routes)):
            if self.routes[i].is_feasible_all() == False:
                unfeasibleRoutes.append(i)
        return unfeasibleRoutes
    
    def removeEmptyRoutes(self):
        for route in self.routes:
            if not any(isinstance(item, Customer) for item in route.route):
                self.routes.remove(route)