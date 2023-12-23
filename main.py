import os
from openpyxl import Workbook
import pandas as pd
import subprocess
from alnsSolution import alns_iterate
from initialsolution import initial_solution
from readProblemInstances import readProblemInstances
from visualize_solution import runEvrtpwVerifier, visualizeAllRoutes, visualizeRoutesSeperately, writeSolution

#GLOBAL VARIABLES FOR ALNS

j=0 #- Number of iterations allowed without improvement
maxIterations=25000
N = maxIterations*0.1 # - Maximum iterations allowed without improvement
K= 4# Predefined iteration interval
Z=2 #Weights update interval

def process_test_file(file_path):
    problemFile = readProblemInstances(file_path)
    solution = initial_solution(problemFile.depot, problemFile.customers, problemFile)

    file_name = os.path.splitext(os.path.basename(file_path))[0].split('_')[0]
    alns_solution=alns_iterate(solution,j,maxIterations,N,K,Z)
    #visualizeAllRoutes(alns_solution.routes,problemFile)
    #visualizeRoutesSeperately(alns_solution.routes,problemFile)
    writeSolution(alns_solution.routes,alns_solution,problemFile,file_name)
    evrtpw_verifier_result=runEvrtpwVerifier(file_name)
    
    return alns_solution,evrtpw_verifier_result

def main():
    folder_path = 'SchneiderData/'
    results = []
    i=0
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            result,evrtpw_verifier_result = process_test_file(file_path)
            results.append({'File': filename, 'Objective Function Value': result.get_Total_Objective_Function_Value(),"Total Distance":result.getTotalDistance(),"Evrtpw Verifier Result":evrtpw_verifier_result})

    df = pd.DataFrame(results)
    output_excel_path = 'SolutionFiles/results.xlsx'
    df.to_excel(output_excel_path, index=False)

if __name__ == "__main__":
    main()