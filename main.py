from AlnsOperators.Operators import CustomerInsertionOperator
from AlnsOperators.RouteOperators import greedyRouteRemovalOperator, randomRouteRemovalOperator
from alnsSolution import alns_iterate
from initialsolution import initial_solution
from readProblemInstances import readProblemInstances
from test_funcs import test_files_in_directory
from visualize_solution import visualizeAllRoutes, visualizeRoutesSeperately, writeSolution
from AlnsOperators.CustomerOperators import Regret_K_Insertion, removeRandomCustomerOperator, leastTimeWindowCustomerRemovalOperator, relatedCustomerRemovalOperator,greedyCustomerInsertionOperator, worstDistanceCustomerRemovalOperator
from AlnsOperators.StationOperators import Compare_K_Insertion, bestStationInsertionOperator, randomStationRemovalOperator, worstChargeUsageStationRemovalOperator, worstStationRemovalOperator

def main():
    data_set_path = "c205C10" 
    problemFile = readProblemInstances('SchneiderData/'+data_set_path+'.txt')  # Değişken atama işlemi düzeltilmiş ve parantez eklendi.
    solution=initial_solution(problemFile.depot,problemFile.customers,problemFile)
    j=0 #- Number of iterations allowed without improvement
    maxIterations=1000
    N = maxIterations*0.1 # - Maximum iterations allowed without improvement
    K= 4# Predefined iteration interval
    Z=2 #Weights update interval

    
    alns_solution=alns_iterate(solution,j,maxIterations,N,K,Z)
    visualizeAllRoutes(alns_solution.routes,problemFile)
    visualizeRoutesSeperately(alns_solution.routes,problemFile)
    writeSolution(alns_solution.routes,alns_solution,problemFile,data_set_path)


    
if __name__ == "__main__":
    main()