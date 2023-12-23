
from AlnsObjects.Route import Route
import os
from openpyxl import Workbook
import pandas as pd
import subprocess
from alnsSolution import alns_iterate
from initialsolution import initial_solution
from readProblemInstances import readProblemInstances
from visualize_solution import visualizeAllRoutes, visualizeRoutesSeperately, writeSolution

def writeSolution(routes,solution, problem_instance,data_set_path):
    """
    Verilen rotaları bir çözüm dosyasına yazan fonksiyon.

    Args:
        routes (list): Rotaları içeren liste.
        problem_instance (RoutingProblemInstance): Rota problemi örneği.
    """
    filePath = "SolutionFiles/"
    dosya_adı = "solution.txt"
    with open(filePath+data_set_path+"_solution"+".txt", 'w') as dosya:
        dosya.write(f"#{data_set_path}")
        dosya.write("\n")
        dosya.write(f"{solution.getTotalDistance()}")
        dosya.write("\n") 
        for i, route in enumerate(routes, start=0):
            j=0
            for location in route.route:
                #veri setinin adını yazdır
                dosya.write(f"{location.id}")
                # Son eleman değilse virgül koy
                if j!=len(route.route)-1:
                    dosya.write(", ")
                j+=1
            dosya.write("\n")  # Her rotanın sonuna satır sonu karakteri
            
    print(f"Dosya '{dosya_adı}' başarıyla oluşturuldu.")

def visualizeAllRoutes(routes, problem_instance):
    """
    Tüm rotaları görselleştiren fonksiyon.

    Args:
        routes (list): Rotaları içeren liste.
        problem_instance (RoutingProblemInstance): Rota problemi örneği.
    """
    route_manager = Route(problem_instance.config, problem_instance.depot) 
    route_manager.route = routes
    route_manager.visualizeAllRoutes()

def visualizeRoutesSeperately(routes, problem_instance):
    """
    Rotaları ayrı ayrı görselleştiren fonksiyon.

    Args:
        routes (list): Rotaları içeren liste.
        problem_instance (RoutingProblemInstance): Rota problemi örneği.
    """
    route_manager = Route(problem_instance.config, problem_instance.depot) 
    route_manager.route = routes
    route_manager.visualizeRoute()

def runEvrtpwVerifier(file_name):
    """
    The `runEvrtpwVerifier` function runs the EVRPTW Verifier tool on a given input file and solution
    file, and returns whether the solution is valid or invalid.
    
    :param file_name: The `file_name` parameter is the name of the input file that will be used as input
    for the EVRPTW Verifier. It should be a string without the file extension
    :return: The function `runEvrtpwVerifier` returns either 'Valid' or 'Invalid' based on the output of
    the EVRPTW Verifier tool.
    """

    jar_path = "EVRPTW_Verifier/evrptw-verifier-0.2.0.jar"
    input_file = f"C:\\Users\\asus\\OneDrive\\Masaüstü\\Github_Repo\\ALNS-Implemantation-On-EVRP\\SchneiderData\\{file_name}.txt"
    solution_file = f"C:\\Users\\asus\\OneDrive\\Masaüstü\\Github_Repo\\ALNS-Implemantation-On-EVRP\\SolutionFiles\\{file_name}_solution.txt"

    # Java JAR dosyasını çalıştırma komutu
    command = ["java", "-jar", jar_path, input_file, solution_file]

    # Terminal komutunu çalıştırma
    result = subprocess.run(command, capture_output=True, text=True)

    # Çıktıları ekrana yazdırma
    print(result.stdout)

    # Hata mesajlarını ekrana yazdırma
    if result.stderr:
        print("Hata Mesajları:")
        print(result.stderr)

    if 'valid' in result.stdout.lower():
        return 'Valid'
    else:
        return 'Invalid'    