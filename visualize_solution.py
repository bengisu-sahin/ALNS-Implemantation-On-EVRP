
from AlnsObjects.Route import Route
import os
from matplotlib import pyplot as plt
import subprocess


from readProblemInstances import readProblemInstances

def writeSolution(routes,solution, problem_instance,data_set_path):
    """
    Verilen rotaları bir çözüm dosyasına yazan fonksiyon.

    Args:
        routes (list): Rotaları içeren liste.
        problem_instance (RoutingProblemInstance): Rota problemi örneği.
    """

    filePath = "SolutionFiles/"
    dosya_adı = data_set_path+"_solution.txt"

    # Klasörü oluştur
    folder_path = os.path.join(filePath, data_set_path)
    os.makedirs(folder_path, exist_ok=True)

    # Dosya yolunu güncelle
    file_path = os.path.join(folder_path, dosya_adı)

    with open(file_path, 'w') as dosya:
        dosya.write(f"#{data_set_path}")
        dosya.write("\n")
        dosya.write(f"{solution.getTotalDistance()}")
        dosya.write("\n")
        for i, route in enumerate(routes, start=0):
            j = 0
            for location in route.route:
                dosya.write(f"{location.id}")
                if j != len(route.route) - 1:
                    dosya.write(", ")
                j += 1
            dosya.write("\n")



def saveVisualizeAllRoutes(routes, problem_instance, file_name):
    """
    Tüm rotaları görselleştiren fonksiyon.

    Args:
        routes (list): Rotaları içeren liste.
        problem_instance (RoutingProblemInstance): Rota problemi örneği.
    """
    route_manager = Route(problem_instance.config, problem_instance.depot) 
    route_manager.route = routes
    route_manager.visualizeAllRoutes(0)
    fig=route_manager.visualizeAllRoutes(0)

    folder_path = os.path.join("SolutionFiles", file_name, "RouteGraphs")
    os.makedirs(folder_path, exist_ok=True) 
    img_path = os.path.join(folder_path, f"AllRoutes_{file_name}.png")
    fig.savefig(img_path)

def saveVisualizeRoutesSeperately(routes, problem_instance, file_name):
    """
    Rotaları ayrı ayrı görselleştiren fonksiyon.

    Args:
        routes (list): Rotaları içeren liste.
        problem_instance (RoutingProblemInstance): Rota problemi örneği.
    """
    route_manager = Route(problem_instance.config, problem_instance.depot) 
    route_manager.route = routes
    figList=route_manager.visualizeRoute()
    # Klasör yolu oluştur
    folder_path = os.path.join("SolutionFiles", file_name, "RouteGraphs")
    os.makedirs(folder_path, exist_ok=True)

    # Her bir figürü ayrı bir dosyaya kaydet
    for i, fig in enumerate(figList, start=1):
        img_path = os.path.join(folder_path, f"Route_{i}.png")
        fig.savefig(img_path)
        plt.close(fig)  # plt.show() kullanılmışsa kapat

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
    input_file = f"./SchneiderData/{file_name}.txt"
    solution_file = f"./SolutionFiles/{file_name}/{file_name}_solution.txt"


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
    
def visualizeAlgorithmProcess(iteration_list, total_distance_list):
    filePath = "SolutionFiles/"
    dosya_adı = "solution.txt"

    # Klasörü oluştur
    #folder_path = os.path.join(filePath, data_set_path)
    # os.makedirs(folder_path, exist_ok=True)
    # plt.plot(iteration_list, total_distance_list, label='Best Solution')
    # plt.xlabel('Iteration')
    # plt.ylabel('Total Distance')
    # plt.title('ALNS Algorithm Progress')
    # plt.legend()
    # plt.show()