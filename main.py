from initialsolution import initial_solution
from readProblemInstances import readProblemInstances
from test_funcs import test_files_in_directory
from visualize_solution import visualizeAllRoutes


def main(): 
    problemFile = readProblemInstances('SchneiderData/r103_21.txt')  # Değişken atama işlemi düzeltilmiş ve parantez eklendi.

    
    dir_list=test_files_in_directory('SchneiderData')
    
    for test in dir_list:
        print(test)
        problemFile = readProblemInstances(test)
        routes=initial_solution(problemFile.depot,problemFile.customers,problemFile)
        

    
if __name__ == "__main__":
    main()