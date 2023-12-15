import random
from AlnsOperators.Operators import RouteOperator


class randomRouteRemovalOperator(RouteOperator):
    def __init__(self):
        super().__init__()

    def remove(self, solution):
        W = self.routeToBeRemoved(solution)
        routes = solution.routes
        routes_to_remove = random.sample(routes, int(W))
        for route in routes_to_remove:
            for customer in route.get_customers():
                solution.routes.unserved_customers.append(customer)
                solution.routes.served.remove(customer)
            routes.remove(route)
        return solution
    

class greedyRouteRemovalOperator(RouteOperator):
    def __init__(self):
        super().__init__()

    def remove(self, solution):
        W = self.routeToBeRemoved(solution)
        routes_to_remove = []
        routesByCustomerNum={}

        for i in range(len(solution.routes)):
            routesByCustomerNum[i] = len(solution.routes[i].get_customers())

        sorted_routes = sorted(routesByCustomerNum.items(), key=lambda x: x[1], reverse=False) # Sort routes by the number of customers ordered by ascending
        removed_greedy_routes = sorted_routes[:W]
        for route in removed_greedy_routes:
            routes_to_remove.append(solution.routes[route[0]])

        for route in routes_to_remove:
            for customer in route.get_customers():
                solution.unserved_customers.append(customer)
                solution.served_customers.remove(customer)
            solution.routes.remove(route)

        return solution