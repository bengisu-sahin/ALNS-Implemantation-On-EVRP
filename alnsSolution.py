import copy
from AlnsObjects.Alns import ALNS
from AlnsOperators.Operators import (
    CustomerInsertionOperator,
    CustomerRemovalOperator,
    RouteOperator,
    StationInsertionOperator,
    StationRemovalOperator,
)


def alns_iterate(
    solution,
    j,
    maxIterations,
    max_iter_without_improvement,
    pre_iter_interval,
    weights_update_interval,
):
    CustomerInsertionOps = CustomerInsertionOperator()
    CustomerRemovalOps = CustomerRemovalOperator()
    StationInsertionOps = StationInsertionOperator()
    StationRemovalOps = StationRemovalOperator()
    RouteOps = RouteOperator()
    bestSolution = copy.deepcopy(solution)
    currentSolution = copy.deepcopy(solution)
    alns = ALNS(bestSolution, currentSolution)
    j = 3
    pre_iter_interval = 3
    max_iter_without_improvement = 2
    totalDistance = currentSolution.getTotalDistance()
    print("Before Improvement: ", totalDistance)
    for i in range(maxIterations):
        if j == max_iter_without_improvement:
            print("Before Improvement: ", totalDistance)
            station_removeOp_index = StationRemovalOps.selectOperator()
            station_removeOp = alns.stationRemovalOps[station_removeOp_index]
            station_removeOp.remove(currentSolution)

            station_insertOp_index = 0

            while currentSolution.isAllRoutesFeasible() == False:
                unfeasibleRoutes = currentSolution.getUnfeasibleRoutes()
                station_insertOp = alns.stationInsertionOps[station_insertOp_index]
                station_insertOp.insert(currentSolution)

            print("After Improvement", currentSolution.getTotalDistance())
        else:
            route_customer_insertOp_index = CustomerInsertionOps.selectOperator()
            route_customer_insertOp = alns.customerInsertionOps[1]

            if j % pre_iter_interval == 0:
                # Call route removal 11
                route_removeOp_index = RouteOps.selectOperator()
                route_removeOp = alns.routeRemovalOps[route_removeOp_index]
                route_removeOp.remove(currentSolution)

                # Call customer insertion 12
                while len(currentSolution.unserved_customers) != 0:
                    unfeasibleRoutes = currentSolution.getUnfeasibleRoutes()
                    route_customer_insertOp.insert(currentSolution)
            
            print("Unfeasible Routes: ", currentSolution.getUnfeasibleRoutes())
            print(currentSolution.getTotalDistance())
            return currentSolution.routes
