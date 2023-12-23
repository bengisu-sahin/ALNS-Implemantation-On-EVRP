
from AlnsObjects.Route import Route


def writeSolution(routes, problem_instance):
    """
    Verilen rotaları bir çözüm dosyasına yazan fonksiyon.

    Args:
        routes (list): Rotaları içeren liste.
        problem_instance (RoutingProblemInstance): Rota problemi örneği.
    """
    filePath = "/SolutionFiles"
    dosya_adı = "solution.txt"
    # Dosyayı açıp içeriği yazma
    with open(dosya_adı, 'w') as dosya:
        # Her bir liste için döngü
        for i, route in enumerate(routes, start=1):
            dosya.write(f"Route {i}: ")  # Her rotanın başlığı
            for location in route.route:
                dosya.write(f"{location.id}, ")  # Her lokasyonun ID'si
            
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