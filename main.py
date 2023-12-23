import os
from openpyxl import Workbook
import pandas as pd
from test_funcs import process_test_file
from pandas import DataFrame


def main():
    #GLOBAL VARIABLES FOR ALNS
    j=5 #- Number of iterations allowed without improvement
    maxIterations=50 # - Maximum number of iterations
    N = maxIterations*0.1 # - Maximum iterations allowed without improvement
    K= 4# Predefined iteration interval
    Z=2 #Weights update interval
    folder_path = 'SchneiderData/'
    results = []
    i=0
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            result,evrtpw_verifier_result = process_test_file(file_path,j,maxIterations,N,K,Z)
            results.append({'File': filename, 'Objective Function Value': result.get_Total_Objective_Function_Value(),"Total Distance":result.getTotalDistance(),"Evrtpw Verifier Result":evrtpw_verifier_result,'j':j,'maxIterations':maxIterations,'N':N,'K':K,'Z':Z})
        i+=1
        if i==2:
            break

    results_df = pd.DataFrame(results)
    output_excel_path = 'SolutionFiles/results.xlsx'
    results_df.to_excel(output_excel_path)

if __name__ == "__main__":
    main()