import copy
import random
from AlnsObjects.Route import Route
from AlnsOperators.Operators import CustomerOperator

# Customer removal operators
class removeRandomCustomerOperator(CustomerOperator):
    def __init__(self):
        super().__init__()

    def remove(self, solution):
        P = int(self.customerToBeRemoved(solution))
        allCustomers=solution.getAllCustomers()
        customers_to_remove = random.sample(allCustomers, int(P))
        
        for route in solution.routes:
            for customer in customers_to_remove:
                if customer in route.route:
                    route.remove_customer_from_route(customer)
        
        self.customerPool.extend(customers_to_remove)
        solution.unserved_customers.extend(self.customerPool)
        solution.served_customers = [customer for customer in solution.served_customers if customer not in self.customerPool]
        return solution.routes
    
class relatedCustomerRemovalOperator(CustomerOperator):
    def __init__(self):
        super().__init__()

    def remove(self, solution):
        P = int(self.customerToBeRemoved(solution))
        allCustomers=solution.getAllCustomers()
        seed_customer = random.choice(allCustomers) #tüm müşterileri döndüren bir fonksiyon yazılmalı rota ya da solution içinde
        distances = {}
        
        for customer in allCustomers:
            if customer != seed_customer:
                distance =customer.distance_to(seed_customer) #customer nesnesinin sahip olduğu distance fonksiyonu kullanılarak mesafe hesaplanıyor.
                distances[customer] = distance #mesafeler bir sözlükte tutuluyor.
        
        sorted_distances = dict(sorted(distances.items(), key=lambda item: item[1])) #mesafelerin küçükten büyüğe sıralanması

        selected_customers = list(sorted_distances.keys())[:P-1] #sıralanmış mesafelerden P-1 tanesi seçiliyor.
        self.customerPool.extend(selected_customers) #seçilen müşteriler customerPool'a ekleniyor.
        solution.unserved_customers.extend(self.customerPool) #seçilen müşteriler unserved_customers'a ekleniyor.
        solution.served_customers = [customer for customer in solution.served_customers if customer not in selected_customers]
        for route in solution.routes:
            for customer in selected_customers:
                if customer in route.route:
                    route.remove_customer_from_route(customer)

        return solution.routes


class leastTimeWindowCustomerRemovalOperator(CustomerOperator):
    def __init__(self):
        super().__init__()

    def remove(self, solution):
        P = int(self.customerToBeRemoved(solution))
        allCustomers=solution.getAllCustomers()
        time_window_gaps = {}
        for customer in allCustomers:
            gap = customer.due_date - customer.ready_time
            time_window_gaps[customer] = gap

        # Sort customers based on time window gaps in ascending order
        sorted_customers = dict(sorted(time_window_gaps.items(), key=lambda item: item[1], reverse=False))
        # Select the first P customers with the least time window gaps
        selected_customers = list(sorted_customers.keys())[:P]
        # Remove the selected customers from the routes
        for route in solution.routes:
            for customer in selected_customers:
                if customer in route.route:
                    route.remove_customer_from_route(customer)

        self.customerPool.extend(selected_customers)
        solution.unserved_customers.extend(selected_customers)
        solution.served_customers = [customer for customer in solution.served_customers if customer not in selected_customers]
        return solution.routes


class worstDistanceCustomerRemovalOperator(CustomerOperator):
    def __init__(self):
        super().__init__()

    def calculate_removal_gain(self,customer, current_solution):
        # Müşterinin çözümde olup olmamasının getirisini hesapla
        # Bu, müşteriyi çözümde bulundurmanın ve bulundurmamanın maliyet farkını içerir
        cost_with_customer = current_solution.calculate_obj_function()
        customerIndex=current_solution.find_item_index_in_solution(customer)
        # Müşteriyi geçici olarak çözümden çıkar 
        current_solution.remove_customer_from_route(customer)      
        cost_without_customer = current_solution.calculate_obj_function()
        
        # Removal gain hesapla
        removal_gain = cost_with_customer - cost_without_customer

        #Müşteriyi çözüme geri ekle
        current_solution.appendcustomer_at_certain_point(customer,customerIndex)
        
        return removal_gain

    def remove(self, solution):
        P = int(self.customerToBeRemoved(solution))
        allCustomers=solution.getAllCustomers()
        removal_gains={}
        for route in solution.routes:
            for item in route.route:
                if item in allCustomers:
                    removal_gains[item.id] = self.calculate_removal_gain(item, route)

        # Removal gain'e göre müşterileri sırala
        sorted_removal_gains = dict(sorted(removal_gains.items(), key=lambda x: x[1], reverse=True))

        # İlk P müşteriyi çözümden çıkar
        removed_customers = [customer for customer in list(sorted_removal_gains.keys())[:P]]
        # Müşterileri çözümden çıkar
        for route in solution.routes:
            for customer in removed_customers:
                if customer in route.route:
                    route.remove_customer_from_route(customer)

        return solution.routes


# Customer insertion operators
class greedyCustomerInsertionOperator(CustomerOperator):
    def __init__(self):
        super().__init__()

    def find_best_insertion_point(self, route, customer):
        min_energy_consumption = float('inf')
        best_insertion_point = -1
        temp_route = copy.copy(route)

        for i in range(1, len(route.route) ):
            temp_route.route = route.route[:i] + [customer] + route.route[i:]
            if(temp_route.is_feasible_all() == False):
                continue
            else:
                # Energy consumption'ı hesapla
                energy_consumption = temp_route.calculate_obj_function()
                
                # Minimum energy consumption'ı kontrol et
                if energy_consumption < min_energy_consumption:
                    min_energy_consumption = energy_consumption
                    best_insertion_point = i

        return best_insertion_point, min_energy_consumption
    
    def insert(self, solution):
        customers = solution.unserved_customers
        random_customer = random.choice(customers)
        best_insertion_info = {}

        for i, route in enumerate(solution.routes):
            best_insertion_point, min_energy_consumption = self.find_best_insertion_point(route, random_customer)
            best_insertion_info[i] = {"point": best_insertion_point, "energy_consumption": min_energy_consumption}

        # En düşük enerji tüketimine sahip rota ve ekleme noktasını bul
        min_energy_route_index = min(best_insertion_info, key=lambda x: best_insertion_info[x]["energy_consumption"])
        best_insertion_point = best_insertion_info[min_energy_route_index]["point"]

        # En uygun rota ve noktaya müşteriyi ekleyin
        best_route = solution.routes[min_energy_route_index]
        solution.routes[min_energy_route_index].appendcustomer_at_certain_point(random_customer, best_insertion_point)
        

        solution.routes[min_energy_route_index] = best_route
        return solution.routes
    

class greedyCustomerInsertionPerturbationOperator(CustomerOperator):
    def __init__(self):
        super().__init__()
        self.perturbation_factor = 0.0

    def find_best_insertion_point(self, route, customer):
            min_energy_consumption = float('inf')
            best_insertion_point = -1
            temp_route = copy.copy(route)

            for i in range(1, len(route.route)):
                temp_route.route = route.route[:i] + [customer] + route.route[i:]
                if(temp_route.is_feasible_all() == False):
                    continue
                else:
                    # Energy consumption'ı hesapla
                    energy_consumption = temp_route.calculate_obj_function()

                    # Minimum energy consumption'ı kontrol et
                    if energy_consumption < min_energy_consumption:
                        min_energy_consumption = energy_consumption
                        best_insertion_point = i

            return best_insertion_point, min_energy_consumption

    def insert(self, solution):
        customers = solution.unserved_customers
        random_customer = random.choice(customers)
        best_insertion_info = {}

        for i, route in enumerate(solution.routes):
            # Generate a new perturbation factor for each iteration
            perturbation_factor = random.uniform(0.8, 1.2)

            best_insertion_point, min_energy_consumption = self.find_best_insertion_point(route, random_customer)
            best_insertion_info[i] = {"point": best_insertion_point, "energy_consumption": min_energy_consumption * perturbation_factor}

        # En düşük enerji tüketimine sahip rota ve ekleme noktasını bul
        min_energy_route_index = min(best_insertion_info, key=lambda x: best_insertion_info[x]["energy_consumption"])
        best_insertion_point = best_insertion_info[min_energy_route_index]["point"]

        # En uygun rota ve noktaya müşteriyi ekleyin
        best_route = solution.routes[min_energy_route_index]

        solution.routes[min_energy_route_index].appendcustomer_at_certain_point(random_customer, best_insertion_point)
        

        solution.routes[min_energy_route_index] = best_route
        return solution.routes