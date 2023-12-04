
from DataObjects.Customer import Customer
from DataObjects.ChargeStation import ChargeStation

class Solution:
    
    def __init__(self,unserved_customers,served_customers, routes, ):
        self.unserved_customers = unserved_customers
        self.served_customers = served_customers
        self.routes = routes
    
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