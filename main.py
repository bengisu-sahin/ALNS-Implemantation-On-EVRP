from initialsolution import initial_solution
from readProblemInstances import readProblemInstances
from visualize_solution import visualizeAllRoutes


def main(): 
    problemFile = readProblemInstances('SchneiderData/c104C10.txt')  # Değişken atama işlemi düzeltilmiş ve parantez eklendi.

    routes=initial_solution(problemFile.depot,problemFile.customers,problemFile)
    visualizeAllRoutes(routes,problemFile)

    
if __name__ == "__main__":
    main()