from AlnsOperators.RouteOperators import greedyRouteRemovalOperator, randomRouteRemovalOperator
from initialsolution import initial_solution
from readProblemInstances import readProblemInstances
from test_funcs import test_files_in_directory
from visualize_solution import visualizeAllRoutes
from AlnsOperators.CustomerOperators import removeRandomCustomerOperator, leastTimeWindowCustomerRemovalOperator, relatedCustomerRemovalOperator,greedyCustomerInsertionOperator,greedyCustomerInsertionPerturbationOperator, worstDistanceCustomerRemovalOperator
from AlnsOperators.StationOperators import bestStationInsertionOperator, randomStationRemovalOperator, worstChargeUsageStationRemovalOperator, worstStationRemovalOperator

def main(): 
    problemFile = readProblemInstances('SchneiderData/c101_21.txt')  # Değişken atama işlemi düzeltilmiş ve parantez eklendi.
    solution=initial_solution(problemFile.depot,problemFile.customers,problemFile)
    total_energy_consumption=0
    #print(type(solution.routes[0]))
    # for route in solution.routes:
    #     total_energy_consumption+=route.calculate_obj_function()
        
    # print("total energy consumption : ",total_energy_consumption)
    # visualizeAllRoutes(solution.routes,problemFile)    
    
    # for test in dir_list:
    #     print(test)
    #     problemFile = readProblemInstances(test)
    #     routes=initial_solution(problemFile.depot,problemFile.customers,problemFile)
    print("*********************************************************************************")
    removeRandomCustomerOp=removeRandomCustomerOperator()   
    # print(solution.routes)
    # print("*********************************************************************************")
    #print(removeRandomCustomerOp.remove(solution))
    
    relatedCustomerRemovalOp=relatedCustomerRemovalOperator()
    leastTimeWindowCustomerRemovalOp=leastTimeWindowCustomerRemovalOperator()
    leastTimeWindowCustomerRemovalOp.remove(solution)
    #print("*********************************************************************************")
    greedyCustomerInsertionOp=greedyCustomerInsertionOperator()
    greedyCustomerInsertionOp.insert(solution)
    # greedyCustomerInsertionPerturbationOp=greedyCustomerInsertionPerturbationOperator()
    # greedyCustomerInsertionPerturbationOp.insert(solution)
    randomStationRemovalOp=randomStationRemovalOperator()
    worstChargeUsageStationRemovalOp=worstChargeUsageStationRemovalOperator()
    worstDistanceCustomerRemovalOp=worstDistanceCustomerRemovalOperator()
    greedyRouteRemovalOp=greedyRouteRemovalOperator()
    randomRouteRemovalOp=randomRouteRemovalOperator()
    bestStationInsertionOp=bestStationInsertionOperator()
    bestStationInsertionOp.insert(solution)
if __name__ == "__main__":
    main()