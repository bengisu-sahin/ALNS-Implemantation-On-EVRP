import os
from openpyxl import Workbook
import pandas as pd
from test_funcs import process_test_file
from pandas import DataFrame


def main():
    #GLOBAL VARIABLES FOR ALNS
    j=0 #- Number of iterations allowed without improvement
    maxIterations=5000 # - Maximum number of iterations
    N =100  # - Maximum iterations allowed without improvement
    K= 50# Predefined iteration interval
    Z=50
    folder_path = 'SchneiderData/'
    results = []
   
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            result,evrtpw_verifier_result = process_test_file(file_path,j,maxIterations,N,K,Z)
            results.append({'File': filename, 'Objective Function Value': result.get_Total_Objective_Function_Value(),"Total Distance":result.getTotalDistance(),"Evrtpw Verifier Result":evrtpw_verifier_result,'j':j,'maxIterations':maxIterations,'N':N,'K':K,'Z':Z})


    results_df = pd.DataFrame(results)
    output_excel_path = 'SolutionFiles/results.xlsx'
    results_df.to_excel(output_excel_path)

if __name__ == "__main__":
    main()