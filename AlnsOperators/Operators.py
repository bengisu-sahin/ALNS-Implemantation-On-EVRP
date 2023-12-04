import random


class CustomerOperator():
    def __init__(self, weights=[], probability=0.0,customerPool=[]):
        self.weights = weights
        self.probability = probability
        self.customerPool = customerPool
        self.P = 0
    
    def customerToBeRemoved(self,solution): #burada solutionState senin yazacağın sınıf olacak. Rotalar burada tutulacak. 
        numOfCustomers = solution.getNumberOfCustomers()
        P=min(0.4 * numOfCustomers, 60)
        return P

    def insertCustomer(self,lst, index, value):
        # Verilen indekse değeri ekleyen manuel ekleme fonksiyonu
        return lst.route[:index] + [value] + lst.route[index:]


class StationOperator():
    def __init__(self, weights=[], probability=0.0):
        self.weights = weights
        self.probability = probability
        self.Q = 0
    
    def stationToBeRemoved(self,solution):
        numOfStations = solution.getNumberOfStation()
        Q=min(0.4 * numOfStations, 10)
        return int(Q)
    
class RouteOperator():
    def __init__(self):
        self.lowerBound = 0
        self.upperBound = 0

    
    def routeToBeRemoved(self,solution):
        Tr=len(solution.routes) #number of routes
        self.lowerBound= int(0.1 * Tr)
        self.upperBound = int(0.4 * Tr)
        W=random.randint(self.lowerBound, self.upperBound)
        return W