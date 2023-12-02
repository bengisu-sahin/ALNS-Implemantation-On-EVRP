
from DataObjects.Customer import Customer


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