from DataObjects.Customer import Customer
from DataObjects.ChargeStation import ChargeStation
from AlnsObjects.Route import Route

def getFeasibleCustomers(unserved_customers, route: Route):
    """
    Verilen rota üzerinde hizmet edilebilir müşterileri döndüren fonksiyon.

    Args:
        unserved_customers (list): Hizmet edilmemiş müşterilerin listesi.
        route (Route): Rota nesnesi.

    Returns:
        list: Hizmet edilebilir müşterilerin listesi.
    """
    feasibleCustomers = []
    for customer in unserved_customers:
        route.route.append(customer)
        route.route.append(route.depot)
        if route.is_feasible() == True:
            feasibleCustomers.append(customer)
        route.route.pop()
        route.route.remove(customer)

    # Hizmet edilebilir müşterileri toplam güç gereksinimine göre sırala

    return feasibleCustomers

def getFeasibleAfterChargeCustomers(unserved_customers, route: Route, problem_instance):
    """
    Şarj istasyonu sonrası hizmet edilebilir müşterileri döndüren fonksiyon.

    Args:
        unserved_customers (list): Hizmet edilmemiş müşterilerin listesi.
        route (Route): Rota nesnesi.
        problem_instance: Problem örneği.

    Returns:
        list: Hizmet edilebilir müşterilerin listesi.
    """
    feasibleCustomers = []
    closest_charge_station = min(problem_instance.charging_stations, key=lambda n: n.distance_to(route.get_last_object()))
    for customer in unserved_customers:
        closest_charge_station = min(problem_instance.charging_stations, key=lambda n: n.distance_to(customer))
        route.route.append(closest_charge_station)
        route.route.append(customer)
        route.route.append(route.depot)
        if route.is_feasible_all() == True:
            feasibleCustomers.append(customer)
        route.route.pop()
        route.route.pop()
        route.route.pop()

    # Hizmet edilebilir müşterileri toplam güç gereksinimine göre sırala

    return feasibleCustomers

def initial_solution(depot, customers, problem_instance):
    """
    Başlangıç çözümünü oluşturan fonksiyon.

    Args:
        depot: Depo nesnesi.
        customers (list): Müşterilerin listesi.
        problem_instance: Problem örneği.

    Returns:
        list: Oluşturulan rotaların listesi.
    """
    routes = []
    served_customers = []
    unserved_customers = customers.copy()

    last_position = min(unserved_customers, key=lambda n: n.distance_to(depot))
    initial_route = Route(problem_instance.config, problem_instance.depot)
    initial_route.route.append(last_position)

    served_customers.append(last_position)
    unserved_customers.remove(last_position)

    while len(served_customers) != len(customers):

        feasibleCustomers = getFeasibleCustomers(unserved_customers, initial_route)
        sorted_feasibleCustomers = sorted(feasibleCustomers, key=lambda n: n.distance_to(initial_route.get_last_object()))
        feasibeAfterChargeCustomers = getFeasibleAfterChargeCustomers(unserved_customers, initial_route, problem_instance)
        sorted_feasibleAfterChargeCustomers = sorted(feasibeAfterChargeCustomers, key=lambda n: n.distance_to(initial_route.get_last_object()))

        if len(feasibleCustomers) == 0:
            initial_route.route.append(depot)
            if initial_route.is_feasible_all() == True:
                routes.append(initial_route)

                initial_route = Route(problem_instance.config, problem_instance.depot)

                sorted_unserved_customers = sorted(unserved_customers, key=lambda n: n.distance_to(depot))
                for customer in sorted_unserved_customers:
                    initial_route.route.append(customer)
                    initial_route.route.append(depot)
                    if initial_route.is_feasible_all() == True:
                        initial_route.route.pop()
                        served_customers.append(customer)
                        unserved_customers.remove(customer)
                        break
                    else:
                        initial_route.route.pop()
                        closest_charge_station = min(problem_instance.charging_stations, key=lambda n: n.distance_to(initial_route.get_last_object()))

                        initial_route.route.pop()
                        initial_route.route.append(closest_charge_station)
                        initial_route.route.append(customer)
                        initial_route.route.append(depot)
                        if initial_route.is_feasible_all() == True:
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
                    initial_route = Route(problem_instance.config, problem_instance.depot)
                    initial_route.route.append(customer)
                    initial_route.route.append(depot)
                    if initial_route.is_feasible_all() == True:
                        initial_route.route.pop()

                        served_customers.append(customer)
                        unserved_customers.remove(customer)
                        break
                    else:
                        initial_route.route.pop()
                        closest_charge_station = min(problem_instance.charging_stations, key=lambda n: n.distance_to(initial_route.get_last_object()))
                        initial_route.route.pop()
                        initial_route.route.append(closest_charge_station)
                        initial_route.route.append(customer)
                        initial_route.route.append(depot)
                        if initial_route.is_feasible_all() == True:
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
    
    return routes

