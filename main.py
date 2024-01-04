import os
from openpyxl import Workbook
import pandas as pd
from test_funcs import process_test_file
from pandas import DataFrame
import time


def main():
    #GLOBAL VARIABLES FOR ALNS
    j=0 #- Number of iterations allowed without improvement
    maxIterations=25000 # - Maximum number of iterations
    N = 1  # - Maximum iterations allowed without improvement
    K = 10  #Predefined iteration interval
    Z=50
    folder_path = 'SchneiderData/'
    test_path = 'SchneiderData/test/'
    results = []
   
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            print(filename)
            start_time = time.time()
            result,evrtpw_verifier_result = process_test_file(file_path,j,maxIterations,N,K,Z)
            end_time = time.time()
            elapsed_time = end_time - start_time
            results.append({'File': filename, 'Objective Function Value': result.get_Total_Objective_Function_Value(),"Total Distance":result.getTotalDistance(),"Evrtpw Verifier Result":evrtpw_verifier_result,'j':j,'maxIterations':maxIterations,'N':N,'K':K,'Z':Z,'Elapsed Time':elapsed_time})


    results_df = pd.DataFrame(results)
    output_excel_path = 'SolutionFiles/results.xlsx'
    results_df.to_excel(output_excel_path)

if __name__ == "__main__":
    main()