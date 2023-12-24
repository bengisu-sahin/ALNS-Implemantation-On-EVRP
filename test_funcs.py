import os
from alnsSolution import alns_iterate

from initialsolution import initial_solution
from readProblemInstances import readProblemInstances
from visualize_solution import runEvrtpwVerifier, saveALNSResultsDevelopment, saveVisualizeAllRoutes, saveVisualizeRoutesSeperately, writeSolution

def process_test_file(file_path,j,maxIterations,N,K,Z):
    

    problemFile = readProblemInstances(file_path)
    solution = initial_solution(problemFile.depot, problemFile.customers, problemFile)

    file_name = os.path.splitext(os.path.basename(file_path))[0]
    alns_solution=alns_iterate(solution,j,maxIterations,N,K,Z)
    saveVisualizeAllRoutes(alns_solution.routes,problemFile,file_name)
    saveVisualizeRoutesSeperately(alns_solution.routes,problemFile,file_name)
    saveALNSResultsDevelopment(alns_solution)
    writeSolution(alns_solution.routes,alns_solution,problemFile,file_name)
    evrtpw_verifier_result=runEvrtpwVerifier(file_name)
    
    return alns_solution,evrtpw_verifier_result


def process_file(file_path):
    # Belirli bir kodu çağırın veya dosya üzerinde istediğiniz işlemleri gerçekleştirin
    # Örnek olarak, dosyanın içeriğini ekrana yazdıralım
    with open(file_path, 'r') as file:
        content = file.read()
        print("file name : ",file_path)
        
def test_files_in_directory(directory):
    # Dizin içindeki tüm dosya adlarını al
    file_list = os.listdir(directory)

    # Dosya adlarını tam dosya yollarına dönüştür
    file_paths = [os.path.join(directory, file) for file in file_list]
    print(file_paths)
    return file_paths