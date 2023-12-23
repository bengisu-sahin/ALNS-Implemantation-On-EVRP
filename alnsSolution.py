import copy

from matplotlib import pyplot as plt
from AlnsObjects.Alns import ALNS
from AlnsOperators.Operators import (
    CustomerInsertionOperator,
    CustomerRemovalOperator,
    RouteOperator,
    StationInsertionOperator,
    StationRemovalOperator,
)


def alns_iterate(solution,j,maxIterations,max_iter_without_improvement,pre_iter_interval,weights_update_interval,):
    CustomerInsertionOps = CustomerInsertionOperator()
    CustomerRemovalOps = CustomerRemovalOperator()
    StationInsertionOps = StationInsertionOperator()
    StationRemovalOps = StationRemovalOperator()
    RouteOps = RouteOperator()
    bestSolution = copy.deepcopy(solution)
    currentSolution = copy.deepcopy(solution)
    iSolution = copy.deepcopy(solution)
    alns = ALNS(bestSolution, currentSolution)
    acceptance_rate = 0.03
    totalDistance = iSolution.getTotalDistance()
    iteration_list = []
    total_distance_list = []
    
    print("Before Improvement: ", totalDistance)
    for i in range(maxIterations):
        iteration_list.append(i)
        iSolution = copy.deepcopy(currentSolution)
        if j == max_iter_without_improvement:
            print("Before Improvement: ", totalDistance)
            station_removeOp_index = StationRemovalOps.selectOperator()
            station_removeOp = alns.stationRemovalOps[station_removeOp_index]
            station_removeOp.remove(iSolution)

            station_insertOp_index = StationInsertionOps.selectOperator()


            for i in range(len(iSolution.getUnfeasibleRoutes())):
                unfeasibleRoutes = iSolution.getUnfeasibleRoutes()
                station_insertOp = alns.stationInsertionOps[station_insertOp_index]
                station_insertOp.insert(iSolution)
            
            if(iSolution.isAllRoutesFeasible() == False):
                iSolution = copy.deepcopy(currentSolution)
            print("After Improvement", iSolution.getTotalDistance())
        else:
            route_customer_insertOp_index = CustomerInsertionOps.selectOperator()
            route_customer_insertOp = alns.customerInsertionOps[route_customer_insertOp_index]

            if j % pre_iter_interval == 0 and j != 0:
                # Call route removal 11
                route_removeOp_index = RouteOps.selectOperator()
                route_removeOp = alns.routeRemovalOps[route_removeOp_index]
                route_removeOp.remove(iSolution)

                # Call customer insertion 12
                while len(iSolution.unserved_customers) != 0:
                    unfeasibleRoutes = iSolution.getUnfeasibleRoutes()
                    route_customer_insertOp.insert(iSolution)
            else:
                # Call customer removal 14
                customer_removeOp_index = CustomerRemovalOps.selectOperator()
                customer_removeOp = alns.customerRemovalOps[customer_removeOp_index]
                customer_removeOp.remove(iSolution)

                # Call customer insertion 15
                while len(iSolution.unserved_customers) != 0:
                    unfeasibleRoutes = iSolution.getUnfeasibleRoutes()
                    route_customer_insertOp.insert(iSolution)
        print("CurrentSolution before improvement total distance: ", currentSolution.getTotalDistance())
        if iSolution.get_Total_Objective_Function_Value() <= (
            currentSolution.get_Total_Objective_Function_Value() * (1 + acceptance_rate)
        ):
            if(j == max_iter_without_improvement):
                alns.stationRemovalOps[station_removeOp_index].score += 3
                alns.stationInsertionOps[station_insertOp_index].score += 3
            else:
                alns.customerInsertionOps[route_customer_insertOp_index].score += 3
                if(j%pre_iter_interval == 0 and j != 0):
                    alns.routeRemovalOps[route_removeOp_index].score += 3
                else:
                    alns.customerRemovalOps[customer_removeOp_index].score += 3
            currentSolution = copy.deepcopy(iSolution)
            j = 0
            # TODO: Update Scores must be implemented here

        elif j == max_iter_without_improvement:
            if(j == max_iter_without_improvement):
                alns.stationRemovalOps[station_removeOp_index].score += 1
                alns.stationInsertionOps[station_insertOp_index].score +=1
            else:
                alns.customerInsertionOps[route_customer_insertOp_index].score += 1
                if(j%pre_iter_interval == 0  and j != 0):
                    alns.routeRemovalOps[route_removeOp_index].score += 1
                else:
                    alns.customerRemovalOps[customer_removeOp_index].score += 1
            currentSolution = copy.deepcopy(iSolution)
            j = 0
            # TODO: Update Scores must be implemented here
        else:
            j += 1

        if (
            currentSolution.get_Total_Objective_Function_Value()
            < bestSolution.get_Total_Objective_Function_Value()
        ):
            bestSolution = copy.deepcopy(currentSolution)

        if i % weights_update_interval == 0 and i!=0:
            # TODO: Update Weights must be implemented here
            for idx, score in enumerate(alns.customerInsertionOps):
                CustomerInsertionOps.weights[idx] += score.score
            
            for idx, score in enumerate(alns.customerRemovalOps):
                CustomerRemovalOps.weights[idx] += score.score

            # Update StationInsertionOps weights
            for idx, score in enumerate(alns.stationInsertionOps):
                StationInsertionOps.weights[idx] += score.score

            # Update StationRemovalOps weights
            for idx, score in enumerate(alns.stationRemovalOps):
                StationRemovalOps.weights[idx] += score.score

            # Update RouteOps weights
            for idx, score in enumerate(alns.routeRemovalOps):
                RouteOps.weights[idx] += score.score
            alns.resetScoresForAllOperators()
            
        total_distance_list.append(bestSolution.getTotalDistance())
        print("Iteration: ", i)
        print("Unfeasible Routes: ", iSolution.getUnfeasibleRoutes())
        print("Best Solution total distance: ",bestSolution.getTotalDistance())
        print("Best solution objective function value: ", bestSolution.get_Total_Objective_Function_Value())
        print("iSolution Solution total distance: ",iSolution.getTotalDistance())
        print("Unserviced Customers: ", bestSolution.getUnservedCustomers())
        print("İteration without improvement: ", j)
        print("-----------------------------")
    print("Best solution unfeasible routes: ", bestSolution.getUnfeasibleRoutes())
    print("Unserviced Customers: ", bestSolution.getUnservedCustomers())
    # plt.plot(iteration_list, total_distance_list, label='Best Solution')
    # plt.xlabel('Iteration')
    # plt.ylabel('Total Distance')
    # plt.title('ALNS Algorithm Progress')
    # plt.legend()
    # plt.show()

    return bestSolution
