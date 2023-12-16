from AlnsOperators.Operators import CustomerInsertionOperator
from AlnsOperators.RouteOperators import greedyRouteRemovalOperator, randomRouteRemovalOperator
from initialsolution import initial_solution
from readProblemInstances import readProblemInstances
from test_funcs import test_files_in_directory
from visualize_solution import visualizeAllRoutes
from AlnsOperators.CustomerOperators import Regret_K_Insertion, removeRandomCustomerOperator, leastTimeWindowCustomerRemovalOperator, relatedCustomerRemovalOperator,greedyCustomerInsertionOperator,greedyCustomerInsertionPerturbationOperator, worstDistanceCustomerRemovalOperator
from AlnsOperators.StationOperators import Compare_K_Insertion, bestStationInsertionOperator, randomStationRemovalOperator, worstChargeUsageStationRemovalOperator, worstStationRemovalOperator

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
    # print("*********************************************************************************")
    # removeRandomCustomerOp=removeRandomCustomerOperator()   
    # print(solution.routes)
    # print("*********************************************************************************")
    #print(removeRandomCustomerOp.remove(solution))
    worstStationRemovalOp=worstStationRemovalOperator()
    worstStationRemovalOp.remove(solution)
    # relatedCustomerRemovalOp=relatedCustomerRemovalOperator()
    # leastTimeWindowCustomerRemovalOp=leastTimeWindowCustomerRemovalOperator()
    # leastTimeWindowCustomerRemovalOp.remove(solution)
    # score=0.0
    # regret=Regret_K_Insertion(k=3,score=score)
    # regret.insert(solution)
    # greedyCustomerInsertionPerturbationOp=greedyCustomerInsertionPerturbationOperator()
    # greedyCustomerInsertionPerturbationOp.insert(solution)
    randomStationRemovalOp=randomStationRemovalOperator()
    randomStationRemovalOp.remove(solution)
    compare_k_charge_station_insertion=Compare_K_Insertion(k=1,score=0)
    compare_k_charge_station_insertion.insert(solution)
    worstChargeUsageStationRemovalOp=worstChargeUsageStationRemovalOperator()
    worstDistanceCustomerRemovalOp=worstDistanceCustomerRemovalOperator()
    greedyRouteRemovalOp=greedyRouteRemovalOperator()
    randomRouteRemovalOp=randomRouteRemovalOperator()


    
if __name__ == "__main__":
    main()