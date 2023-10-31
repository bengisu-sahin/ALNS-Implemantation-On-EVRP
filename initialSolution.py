from AlnsObjects.Route import Route
from problemInstances import RoutingProblemInstance

def find_closest_customer(problemInstances):
    depot = problemInstances.depot
    customers = problemInstances.customers

    # En yakın müşteriyi ve mesafeyi sıfırla
    closest_customer = None
    closest_distance = float('inf')

    # Her müşteriyi gezerek en yakın müşteriyi bul
    for customer in customers:
        distance = customer.distance_to(depot)
        if distance < closest_distance:
            closest_customer = customer
            closest_distance = distance

    return closest_customer

def initialSolution(problemInstances: RoutingProblemInstance):
    unserved_customers = problemInstances.customers.copy()

    initial_route = Route(problemInstances.config,problemInstances.depot)
    depot=problemInstances.customers[0]
    closest_customer = find_closest_customer(problemInstances)
    initial_route.route.append(closest_customer) #ilk olarak depoya en yakın customer ı başlangıç çözümüne ekle
    unserved_customers.remove(closest_customer)

    for customer in unserved_customers:
        initial_route.route.append(customer)
        feasible_customers=initial_route.is_feasible()
    if not feasible_customers:
        initial_route.route.pop()
    

    print("Başlangıç Rota:")
    for point in initial_route.route:
        print(point)

    return True