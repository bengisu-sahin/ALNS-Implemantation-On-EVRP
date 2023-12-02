from initialsolution import initial_solution
from readProblemInstances import readProblemInstances
from test_funcs import test_files_in_directory
from visualize_solution import visualizeAllRoutes


def main(): 
    problemFile = readProblemInstances('SchneiderData/c101_21.txt')  # Değişken atama işlemi düzeltilmiş ve parantez eklendi.
    solution=initial_solution(problemFile.depot,problemFile.customers,problemFile)
    total_energy_consumption=0
    for route in solution.routes:
        total_energy_consumption+=route.calculate_obj_function()
        
    print("total energy consumption : ",total_energy_consumption)
    visualizeAllRoutes(solution.routes,problemFile)    
    
    # for test in dir_list:
    #     print(test)
    #     problemFile = readProblemInstances(test)
    #     routes=initial_solution(problemFile.depot,problemFile.customers,problemFile)
        

    
if __name__ == "__main__":
    main()