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
    j = 2
    max_iter_without_improvement = 2
    for i in range(maxIterations):
        if j == max_iter_without_improvement:
            station_removeOp_index = StationRemovalOps.selectOperator()
            station_removeOp = alns.stationRemovalOps[station_removeOp_index]
            station_removeOp.remove(currentSolution)

            station_insertOp_index = 0

            while currentSolution.isAllRoutesFeasible() == False:
                unfeasibleRoutes = currentSolution.getUnfeasibleRoutes()
                station_insertOp = alns.stationInsertionOps[station_insertOp_index]
                station_insertOp.insert(currentSolution)

            (
                feasiblecount,
                unfeasiblecount,
            ) = currentSolution.getnumberofFeasibleAndUnfeasibleRoutes()

            return currentSolution.routes
