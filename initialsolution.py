from DataObjects.Customer import Customer
from DataObjects.ChargeStation import ChargeStation
from mathmodels import calculate_remaining_tank_capacity
from AlnsObjects.Route import Route





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




def initial_solution(depot,customers,problem_instance):
    last_position=depot
    routes=[]
    served_customers=[]
    unserved_customers=customers.copy()
        
    
    while len(served_customers)!=len(customers):
        last_position=depot
        initial_route = Route(problem_instance.config,problem_instance.depot)
        
       
        last_position=min(unserved_customers, key=lambda n: n.distance_to(last_position))
        
        initial_route.route.append(last_position)
        served_customers.append(last_position)
        unserved_customers.remove(last_position)
    
        while len(served_customers)!=len(customers):
                
            feasibleCustomers= getFeasibleCustomers(unserved_customers,initial_route)
                
            
            if(len(feasibleCustomers)==0):
                initial_route.route.append(depot)
                routes.append(initial_route)
                break
            else: 
                sorted_feasibleCustomers=sorted(feasibleCustomers, key=lambda n: n.distance_to(last_position))
                next_position=sorted_feasibleCustomers[0]
                last_position=next_position
                initial_route.route.append(next_position)
               
                closest_charge_station=min(problem_instance.charging_stations, key=lambda n: n.distance_to(next_position))
                if(initial_route.tank_capacity_constraint_violated()==False):
                    served_customers.append(next_position)
                    unserved_customers.remove(next_position)
                else:
                    initial_route.route.remove(next_position)
                    initial_route.route.append(closest_charge_station)
                    initial_route.route.append(next_position)
                    if(initial_route.is_feasible()==True):
                        if(initial_route.tank_capacity_constraint_violated()==False):
                            served_customers.append(next_position)
                            unserved_customers.remove(next_position)
                        else:
                            initial_route.route.remove(next_position)
                            initial_route.route.remove(closest_charge_station)
                            initial_route.route.append(depot)
                            routes.append(initial_route)
                            break
                    else:
                        initial_route.route.remove(next_position)
                        initial_route.route.append(depot)
                        routes.append(initial_route)
                        break
                        
        
    total_distance=0
    for route in routes:
        if(route.is_feasible_all()==True):
            print(route.route)
        else:
            print("Infeasible Route")
    print("Total Distance: ",total_distance)
    return routes
    