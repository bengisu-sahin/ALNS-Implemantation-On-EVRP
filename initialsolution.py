from DataObjects.Customer import Customer
from DataObjects.ChargeStation import ChargeStation
from mathmodels import calculate_remaining_tank_capacity
from AlnsObjects.Route import Route

def writeSolution(routes,problem_instance):
    filePath="/SolutionFiles"
    dosya_adı = "solution.txt"
    # Dosyayı açıp içeriği yazma
    with open(dosya_adı, 'w') as dosya:
        # Her bir liste için döngü
        for i, route in enumerate(routes, start=1):
            dosya.write(f"Route {i}: ")  # Her rotanın başlığı
            for location in route.route:
                dosya.write(f"{location.id} ({location.x}, {location.y}) -> ")  # Her lokasyonun ID'si
            
            dosya.write("D0\n\n")  # Her rotanın sonu ve başlangıç noktası


    print(f"Dosya '{dosya_adı}' başarıyla oluşturuldu.")

def visualizeAllRoutes(routes,problem_instance):
    route_manager = Route(problem_instance.config,problem_instance.depot) 
    route_manager.route = routes
    route_manager.visualizeAllRoutes()

def visualizeRoutesSeperately(routes,problem_instance):
    route_manager = Route(problem_instance.config,problem_instance.depot) 
    route_manager.route = routes
    route_manager.visualizeRoute()

def getFeasibleCustomers(unserved_customers,route:Route):
    feasibleCustomers=[]
    for customer in unserved_customers:
        route.route.append(customer)
        route.route.append(route.depot)
        if route.is_feasible()==True:
            feasibleCustomers.append(customer)
        route.route.pop()
        route.route.remove(customer)
        
    #sort feasible customers based on total power required to serve them
    
    return feasibleCustomers

def getFeasibleAfterChargeCustomers(unserved_customers,route:Route,problem_instance):
    feasibleCustomers=[]
    closest_charge_station=min(problem_instance.charging_stations, key=lambda n: n.distance_to(route.get_last_object()))
    for customer in unserved_customers:
        closest_charge_station=min(problem_instance.charging_stations, key=lambda n: n.distance_to(customer))
        route.route.append(closest_charge_station)
        route.route.append(customer)
        route.route.append(route.depot)
        if route.is_feasible_all()==True:
            feasibleCustomers.append(customer)
        route.route.pop()
        route.route.pop()
        route.route.pop()
        
    #sort feasible customers based on total power required to serve them
    
    return feasibleCustomers




def initial_solution(depot,customers,problem_instance):

    routes=[]
    served_customers=[]
    unserved_customers=customers.copy()
    
    last_position=min(unserved_customers, key=lambda n: n.distance_to(depot))
    initial_route = Route(problem_instance.config,problem_instance.depot)    
    initial_route.route.append(last_position)
    
    served_customers.append(last_position)
    unserved_customers.remove(last_position)
   
    while len(served_customers)!=len(customers):
        
        feasibleCustomers= getFeasibleCustomers(unserved_customers,initial_route)
        sorted_feasibleCustomers=sorted(feasibleCustomers, key=lambda n: n.distance_to(initial_route.get_last_object()))
        feasibeAfterChargeCustomers=getFeasibleAfterChargeCustomers(unserved_customers,initial_route,problem_instance)
        sorted_feasibleAfterChargeCustomers=sorted(feasibeAfterChargeCustomers, key=lambda n: n.distance_to(initial_route.get_last_object()))
      

        if( len(feasibleCustomers)==0):
            initial_route.route.append(depot)
            if(initial_route.is_feasible_all()==True):
                routes.append(initial_route)


                initial_route = Route(problem_instance.config,problem_instance.depot)
                
                sorted_unserved_customers=sorted(unserved_customers, key=lambda n: n.distance_to(depot))
                for customer in sorted_unserved_customers:
                     initial_route.route.append(customer)
                     initial_route.route.append(depot)
                     if(initial_route.is_feasible_all()==True):
                            initial_route.route.pop()
                            served_customers.append(customer)
                            unserved_customers.remove(customer)
                            break
                     else:
                            initial_route.route.pop()
                            closest_charge_station=min(problem_instance.charging_stations, key=lambda n: n.distance_to(initial_route.get_last_object()))

                            initial_route.route.pop()
                            initial_route.route.append(closest_charge_station)
                            initial_route.route.append(customer)
                            initial_route.route.append(depot)
                            if(initial_route.is_feasible_all()==True):
                                initial_route.route.pop()
                                served_customers.append(customer)
                                unserved_customers.remove(customer)
                                break
                            else:
                                initial_route.route.pop()
                                initial_route.route.pop()
                                initial_route.route.pop()
                           

            else:
                initial_route.route.pop()
                for customer in unserved_customers:
                    initial_route = Route(problem_instance.config,problem_instance.depot)
                    initial_route.route.append(customer)
                    initial_route.route.append(depot)
                    if(initial_route.is_feasible_all()==True):
                        initial_route.route.pop()
                        
                        served_customers.append(customer)
                        unserved_customers.remove(customer)
                        break
                    else:
                        initial_route.route.pop()
                        closest_charge_station=min(problem_instance.charging_stations, key=lambda n: n.distance_to(initial_route.get_last_object()))
                        initial_route.route.pop()
                        initial_route.route.append(closest_charge_station)
                        initial_route.route.append(customer)
                        initial_route.route.append(depot)
                        if(initial_route.is_feasible_all()==True):
                            initial_route.route.pop()
                            
                            served_customers.append(customer)
                            unserved_customers.remove(customer)
                            break
                        else:
                            initial_route.route.pop()
                            initial_route.route.pop()
                            initial_route.route.pop()
                            if(customer==unserved_customers[-1]):    
                                initial_route.route.append(depot)
                                if(initial_route.is_feasible_all()==True):
                                    initial_route.route.pop()
                                    served_customers.append(customer)
                                    unserved_customers.remove(customer)
                                    break
                                else:
                          
                                    break
                            
                
                
        else:
            for customer in sorted_feasibleCustomers:
                initial_route.route.append(customer)
                initial_route.route.append(depot)
                if(initial_route.is_feasible()==True):
                    if(initial_route.is_feasible_all()==True):
                        initial_route.route.pop()
                        served_customers.append(customer)
                        unserved_customers.remove(customer)
                        break
                    else:
                        initial_route.route.pop()
                        closest_charge_station=min(problem_instance.charging_stations, key=lambda n: n.distance_to(initial_route.get_last_object()))
                        initial_route.route.pop()
                        
                        initial_route.route.append(closest_charge_station)
                        initial_route.route.append(customer)
                        initial_route.route.append(depot)
                        if(initial_route.is_feasible_all()==True):
                            initial_route.route.pop()
                            served_customers.append(customer)
                            unserved_customers.remove(customer)
                            break
                        else:
                            initial_route.route.pop()
                            initial_route.route.pop()
                            initial_route.route.pop()
                            if(customer==sorted_feasibleCustomers[-1]):    
                                initial_route.route.append(depot)
                                routes.append(initial_route)
                                sorted_unserviced_customers=sorted(unserved_customers, key=lambda n: n.distance_to(depot))
                                #fix this
                                for customer in sorted_unserviced_customers:
                                    initial_route = Route(problem_instance.config,problem_instance.depot)    
                                    initial_route.route.append(customer)
                                    initial_route.route.append(depot)
                                    if(initial_route.is_feasible_all()==True):
                                        initial_route.route.pop()
                                        served_customers.append(customer)
                                        unserved_customers.remove(customer)
                                        break
                                    else:
                                        initial_route.route.pop()
                                        closest_charge_station=min(problem_instance.charging_stations, key=lambda n: n.distance_to(initial_route.get_last_object()))
                                        initial_route.route.pop()
                                        initial_route.route.append(closest_charge_station)
                                        initial_route.route.append(customer)
                                        initial_route.route.append(depot) 
                                        if(initial_route.is_feasible_all()==True):
                                            initial_route.route.pop()
                                            served_customers.append(customer)
                                            unserved_customers.remove(customer)
                                            break
                                        else:
                                            initial_route.route.pop()
                                            initial_route.route.pop()
                                            initial_route.route.pop()
                                            if(customer==unserved_customers[-1]):    
                                                initial_route.route.append(depot)
                                                if(initial_route.is_feasible_all()==True):
                                                    initial_route.route.pop()
                                                    served_customers.append(customer)
                                                    unserved_customers.remove(customer)
                                                    break
                                                else:
                          
                                                    break
                                        
                                    break
                
                            
                            
                else:
                    initial_route.route.pop()
                    initial_route.route.pop()           
        
    initial_route.route.append(depot)
    routes.append(initial_route)     
        
    total_distance=0 
        
    for route in routes:
        if(route.is_feasible_all()==True):
            charge_stations=route.get_charge_stations()
            total_distance+=route.calculate_total_distance()
            for customer in route.route:
                if(customer!=route.depot and charge_stations.count(customer)==0):
                    print(customer.id)
    total_distance=0
    for route in routes:
        if(route.is_feasible_all()==True):
            print("Route is feasible",routes.index(route))
            total_distance+=route.calculate_total_distance()
               
        else:
            print("Infeasible Route",routes.index(route))
            total_distance+=route.calculate_total_distance()
    
    print("Total Distance: ",total_distance)
    visualizeAllRoutes(routes,problem_instance)
    visualizeRoutesSeperately(routes,problem_instance)
    writeSolution(routes,problem_instance)
    return routes

