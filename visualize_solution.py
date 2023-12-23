
from AlnsObjects.Route import Route


def writeSolution(routes,solution, problem_instance,data_set_path):
    """
    Verilen rotaları bir çözüm dosyasına yazan fonksiyon.

    Args:
        routes (list): Rotaları içeren liste.
        problem_instance (RoutingProblemInstance): Rota problemi örneği.
    """
    filePath = "SolutionFiles/"
    dosya_adı = "solution.txt"
    # Dosyayı açıp içeriği yazma
    with open(filePath+data_set_path+"_solution"+".txt", 'w') as dosya:
        # Her bir liste için döngü
        dosya.write(f"#{data_set_path}")
        dosya.write("\n")
        dosya.write(f"{solution.getTotalDistance()}")
        dosya.write("\n")  # Her rotanın sonuna satır sonu karakteri
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