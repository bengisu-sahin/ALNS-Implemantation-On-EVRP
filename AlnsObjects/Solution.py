
from DataObjects.Customer import Customer
from DataObjects.ChargeStation import ChargeStation

class Solution:
    
    def __init__(self,unserved_customers,served_customers, routes,problemFile ):
        self.unserved_customers = unserved_customers
        self.served_customers = served_customers
        self.routes = routes
        self.problemFile = problemFile
    
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
    
    def getAllStations(self):
        allStations=[]
        for route in self.routes:
            for item in route.route:
                if type(item) is ChargeStation and item not in allStations:
                    allStations.append(item)
        return allStations
    
    def getAllStationInProblemFile(self):
        return self.problemFile.charging_stations
    
    def getAllCustomersInProblemFile(self):
        return self.problemFile.customers
    
    def removeEmptyRoutes(self):
        for route in self.routes:
            if len(route.route) == 0:
                self.routes.remove(route)