import copy
import random
from AlnsObjects.Route import Route
from AlnsOperators.Operators import CustomerInsertionOperator, CustomerRemovalOperator


# Customer removal operators
class removeRandomCustomerOperator(CustomerRemovalOperator):
    def __init__(self, score=0.0):
        super().__init__()
        self.score = score

    def remove(self, solution):
        P = int(self.customerToBeRemoved(solution))
        allCustomers = solution.getAllCustomers()
        customers_to_remove = random.sample(allCustomers, int(P))

        for route in solution.routes:
            for customer in customers_to_remove:
                if customer in route.route:
                    route.remove_customer_from_route(customer)
        
        
        for customer in customers_to_remove:
            solution.unserved_customers.append(customer)
            solution.remove_w_id_served(customer)      

        solution.removeEmptyRoutes()
        return solution


class relatedCustomerRemovalOperator(CustomerRemovalOperator):
    def __init__(self, score=0.0):
        super().__init__()
        self.score = score

    def remove(self, solution):
        P = int(self.customerToBeRemoved(solution))
        allCustomers = solution.getAllCustomers()
        # tüm müşterileri döndüren bir fonksiyon yazılmalı rota ya da solution içinde
        seed_customer = random.choice(allCustomers)
        distances = {}

        for customer in allCustomers:
            if customer != seed_customer:
                # customer nesnesinin sahip olduğu distance fonksiyonu kullanılarak mesafe hesaplanıyor.
                distance = customer.distance_to(seed_customer)
                # mesafeler bir sözlükte tutuluyor.
                distances[customer] = distance

        # mesafelerin küçükten büyüğe sıralanması
        sorted_distances = dict(sorted(distances.items(), key=lambda item: item[1]))

        # sıralanmış mesafelerden P-1 tanesi seçiliyor.
        selected_customers = list(sorted_distances.keys())[: P - 1]
        for customer in selected_customers:
            solution.unserved_customers.append(customer)
            solution.remove_w_id_served(customer)
        
        for route in solution.routes:
            for customer in selected_customers:
                if customer in route.route:
                    route.remove_customer_from_route(customer)
        solution.removeEmptyRoutes()
        return solution


class leastTimeWindowCustomerRemovalOperator(CustomerRemovalOperator):
    def __init__(self, score=0.0):
        super().__init__()
        self.score = score

    def remove(self, solution):
        P = int(self.customerToBeRemoved(solution))
        allCustomers = solution.getAllCustomers()
        time_window_gaps = {}
        for customer in allCustomers:
            gap = customer.due_date - customer.ready_time
            time_window_gaps[customer] = gap

        # Sort customers based on time window gaps in ascending order
        sorted_customers = dict(
            sorted(time_window_gaps.items(), key=lambda item: item[1], reverse=False)
        )
        # Select the first P customers with the least time window gaps
        selected_customers = list(sorted_customers.keys())[:P]
        # Remove the selected customers from the routes
        for route in solution.routes:
            for customer in selected_customers:
                if customer in route.route:
                    route.remove_customer_from_route(customer)

        for customer in selected_customers:
            solution.unserved_customers.append(customer)
            solution.remove_w_id_served(customer)

        solution.removeEmptyRoutes()
        return solution


class worstDistanceCustomerRemovalOperator(CustomerRemovalOperator):
    def __init__(self, score=0.0):
        super().__init__()
        self.score = score

    def calculate_removal_gain(self, customer, current_solution):
        # Müşterinin çözümde olup olmamasının getirisini hesapla
        # Bu, müşteriyi çözümde bulundurmanın ve bulundurmamanın maliyet farkını içerir
        cost_with_customer = current_solution.calculate_obj_function()
        customerIndex = current_solution.find_item_index_in_solution(customer)
        # Müşteriyi geçici olarak çözümden çıkar
        current_solution.remove_customer_from_route(customer)
        cost_without_customer = current_solution.calculate_obj_function()

        # Removal gain hesapla
        removal_gain = cost_with_customer - cost_without_customer

        # Müşteriyi çözüme geri ekle
        current_solution.appendcustomer_at_certain_point(customer, customerIndex)

        return removal_gain

    def remove(self, solution):
        P = int(self.customerToBeRemoved(solution))
        allCustomers = solution.getAllCustomers()
        removal_gains = {}
        for route in solution.routes:
            for item in route.route:
                if item in allCustomers:
                    removal_gains[item] = self.calculate_removal_gain(item, route)

        # Removal gain'e göre müşterileri sırala
        sorted_removal_gains = dict(
            sorted(removal_gains.items(), key=lambda x: x[1], reverse=True)
        )

        # İlk P müşteriyi çözümden çıkar
        removed_customers = [
            customer for customer in list(sorted_removal_gains.keys())[:P]
        ]
        # Müşterileri çözümden çıkar
        for route in solution.routes:
            for customer in removed_customers:
                if customer in route.route:
                    route.remove_customer_from_route(customer)
                    solution.unserved_customers.append(customer)
                    solution.remove_w_id_unserved(customer)

        for customer in removed_customers:
            solution.unserved_customers.append(customer)
            solution.remove_w_id_served(customer)
                        
        solution.removeEmptyRoutes()
        return solution


# Customer insertion operators
class greedyCustomerInsertionOperator(CustomerInsertionOperator):
    def __init__(self, stations=[], score=0.0):
        super().__init__()
        self.stations = stations
        self.score = score

    def getStations(self, solution):
        return solution.getAllStationInProblemFile()

    def find_best_insertion_point(self, route, customer):
        min_energy_consumption = float("inf")
        best_insertion_point = -1
        temp_route = copy.deepcopy(route.route)
        energy_consumption_wihout_insertion = route.calculate_obj_function()
        newRoute = Route(route.config, route.depot)

        for i in range(1, len(route.route)):
            # sırayla müşterileri rotaya ekleyerek en uygun ekleme noktasını bulmaya çalışıyoruz.
            route.appendcustomer_at_certain_point(customer, i)
            if (
                route.is_feasible() == False
            ):  # time window ve payload constraint'lerini kontrol et bunlarda sorun varsa yapılacak bir şey yok zaten yani zaman sınırını ya da yük sınırını değiştirebileceğimiz bir durum yok o sebeple eğer bu if bloğuna girerse müşteriyi rotaya eklemiyoruz. Yeni indeks için tekrar döngüye giriyoruz.
                route.remove_customer_from_route(customer)
                continue
            else:
                if (
                    route.tank_capacity_constraint_violated() == True
                ):  # buraya girdiyse bu şu demek load ve time kısıtlarında sıkıntı yok ama tank capacity kısıtlarında sıkıntı var. Bu durumda en yakın şarj istasyonunu bulup rotaya ekleyip bu durumu düzeltmeye çalışıyoruz. Eğer bu durumda da rotanın feasible olması için bir şey yapamıyorsak yani şarj istasyonu ekledikten sonra da feasible olmuyorsa o zaman müşteriyi rotaya eklemiyoruz ve yeni indeks için tekrar döngüye giriyoruz.
                    newRoute.route = route.route[:i]
                    k = i
                    for index, item in enumerate(route.route[i:], start=i):
                        newRoute.route.append(item)
                        if newRoute.is_feasible_all() == True:
                            continue
                        else:
                            if (
                                newRoute.is_feasible() == True
                                and newRoute.tank_capacity_constraint_violated() == True
                            ):
                                charging_stations_sorted = sorted(
                                    self.stations,
                                    key=lambda station: station.distance_to(
                                        newRoute.route[index - 1]
                                    ),
                                )
                                for station in charging_stations_sorted:
                                    newRoute.append_charge_station_at_certain_point(
                                        station, index
                                    )
                                    if newRoute.is_feasible_all() == True:
                                        break
                                    else:
                                        newRoute.remove_charge_station_from_route_at_certain_point(
                                            index
                                        )
                                        continue
                                if newRoute.is_feasible_all() == False:
                                    break
                    if newRoute.is_feasible_all() == True and len(
                        newRoute.route
                    ) >= len(route.route):
                        energy_consumption_with_insertion = (
                            newRoute.calculate_obj_function()
                        )
                        diff = (
                            energy_consumption_with_insertion
                            - energy_consumption_wihout_insertion
                        )
                        if diff < min_energy_consumption:
                            min_energy_consumption = diff
                            best_insertion_point = i
                        temp_route = copy.copy(newRoute.route)
                        route.remove_customer_from_route(customer)
                else:
                    # Energy consumption'ı hesapla
                    energy_consumption_with_insertion = route.calculate_obj_function()
                    diff = (
                        energy_consumption_with_insertion
                        - energy_consumption_wihout_insertion
                    )
                    # Minimum energy consumption'ı kontrol et
                    if diff < min_energy_consumption:
                        min_energy_consumption = energy_consumption_with_insertion
                        # en uygun ekleme noktasını bulduk. Bu noktaya müşteriyi ekleyeceğiz.
                        best_insertion_point = i
                        # en uygun ekleme noktasını bulduk. Bu noktaya müşteriyi ekleyeceğiz.
                        temp_route = copy.copy(route.route)
                        route.remove_customer_from_route(customer)

        # en uygun ekleme noktasını ve en düşük enerji tüketimini döndürüyoruz.
        return min_energy_consumption, temp_route

    def insert(self, solution):
        # Bunu test ederken denemek için yaptım silinecek
        if len(solution.unserved_customers) == 0:
            customers = solution.served_customers
        else:
            customers = solution.unserved_customers

        random_customer = random.choice(customers)
        best_insertion_info = {}
        # tüm şarj istasyonlarını problem veri setinden alıyoruz
        self.stations = self.getStations(solution)
        for i, route in enumerate(solution.routes):
            min_energy_consumption, newRoute = self.find_best_insertion_point(
                route, random_customer
            )
            best_insertion_info[i] = {
                "point": i,
                "energy_consumption": min_energy_consumption,
                "route": newRoute,
            }

        # En düşük enerji tüketimine sahip rota ve ekleme noktasını bul
        sorted_best_insertion_info = {
            k: v
            for k, v in sorted(
                best_insertion_info.items(),
                key=lambda item: item[1]["energy_consumption"],
            )
        }

        # En uygun rota ve noktaya müşteriyi ekle
        first_route_key, first_route_data = next(
            iter(sorted_best_insertion_info.items())
        )
        best_route = first_route_data["route"]
        solution.routes[first_route_key].route = best_route
        solution.unserved_customers.remove_w_id_unserved(random_customer)
        solution.served_customers.append(random_customer)
        return solution


class Regret_K_Insertion(CustomerInsertionOperator):
    def __init__(self, k, score=0.0):
        super().__init__()
        self.k = k
        self.score = score

    def get_costs(self, customers, stations, solution):
        costs = []
        route_index = 0
        for customer in customers:
            route_index = 0
            for route in solution.routes:
                for i in range(1, len(route.route)):
                    route.appendcustomer_at_certain_point(customer, i)
                    if route.is_feasible() == False:
                        route.remove_customer_from_route(customer)

                        continue
                    else:
                        temp_route = copy.copy(route)
                        temp_route.route = route.route.copy()

                        if temp_route.tank_capacity_constraint_violated() == True:
                            get_closest_station = sorted(
                                stations,
                                key=lambda station: station.distance_to_avg_of_two(
                                    temp_route.route[i], temp_route.route[i - 1]
                                ),
                            )
                            route.append_charge_station_at_certain_point(
                                get_closest_station[0], i
                            )
                            temp_route = copy.copy(route)
                            temp_route.route = route.route.copy()
                            if route.is_feasible_all() == False:
                                route.remove_charge_station_from_route_at_certain_point(
                                    i
                                )
                                temp_route = copy.copy(route)
                                temp_route.route = route.route.copy()
                                get_closest_station = sorted(
                                    stations,
                                    key=lambda station: station.distance_to_avg_of_two(
                                        temp_route.route[i + 1], temp_route.route[i]
                                    ),
                                )
                                route.append_charge_station_at_certain_point(
                                    get_closest_station[0], i + 1
                                )
                                temp_route = copy.copy(route)
                                temp_route.route = route.route.copy()
                                if route.is_feasible_all() == False:
                                    route.remove_charge_station_from_route_at_certain_point(
                                        i + 1
                                    )
                                    route.remove_customer_from_route(customer)
                                    continue
                                else:
                                    costs.append(
                                        (
                                            temp_route.calculate_obj_function(),
                                            temp_route,
                                            customer,
                                            route_index,
                                        )
                                    )
                                    route.remove_customer_from_route(customer)
                                    route.remove_charge_station_from_route_at_certain_point(
                                        i
                                    )

                            else:
                                temp_route = copy.copy(route)
                                temp_route.route = route.route.copy()
                                route.remove_charge_station_from_route_at_certain_point(
                                    i
                                )
                                route.remove_customer_from_route(customer)
                                costs.append(
                                    (
                                        temp_route.calculate_obj_function(),
                                        temp_route,
                                        customer,
                                        route_index,
                                    )
                                )

                        else:
                            costs.append(
                                (
                                    temp_route.calculate_obj_function(),
                                    temp_route,
                                    customer,
                                    route_index,
                                )
                            )
                            route.remove_customer_from_route(customer)
                route_index += 1

        return costs

    def insert(self, solution):
        customers = solution.unserved_customers
        stations = solution.problemFile.charging_stations

        costs = self.get_costs(customers, stations, solution)

        if len(costs) == 0:
            for unserved_customer in solution.unserved_customers:
                for route_index, route in enumerate(solution.routes):
                    temp_route = copy.deepcopy(route)
                    for index, item in enumerate(route.route, start=1):
                        temp_route.route.insert(index, unserved_customer)
                        if temp_route.is_feasible_all() == True:
                            costs.append(
                                (
                                    temp_route.calculate_obj_function(),
                                    copy.deepcopy(temp_route),
                                    unserved_customer,
                                    route_index,
                                )
                            )
                            temp_route.route.remove(unserved_customer)
                        else:
                            if temp_route.tank_capacity_constraint_violated() == True:
                                charging_stations_sorted = sorted(
                                    stations,
                                    key=lambda station: station.distance_to(
                                        temp_route.route[index]
                                    ),
                                )
                                for station in charging_stations_sorted:
                                    temp_route.append_charge_station_at_certain_point(
                                        station, index
                                    )
                                    if temp_route.is_feasible_all() == True:
                                        costs.append(
                                            (
                                                temp_route.calculate_obj_function(),
                                                copy.deepcopy(temp_route),
                                                unserved_customer,
                                                route_index,
                                            )
                                        )
                                        temp_route.remove_charge_station_from_route_at_certain_point(
                                            index
                                        )
                                    else:
                                        temp_route.remove_charge_station_from_route_at_certain_point(
                                            index
                                        )
                                        continue
                                if temp_route.is_feasible_all() == False:
                                    temp_route.route.remove(unserved_customer)
                                else:
                                    costs.append(
                                        (
                                            temp_route.calculate_obj_function(),
                                            copy.deepcopy(temp_route),
                                            unserved_customer,
                                            route_index,
                                        )
                                    )
                                    temp_route.route.remove(unserved_customer)

        if len(costs) == 0:
            while len(solution.unserved_customers) != 0:
                for unserved_customer in solution.unserved_customers:
                    newRoute = Route(
                        solution.problemFile.config, solution.problemFile.depot
                    )
                    newRoute.route.append(unserved_customer)
                    newRoute.route.append(solution.problemFile.depot)
                    if newRoute.is_feasible() == False:
                        continue
                    else:
                        if newRoute.is_feasible_all() == False:
                            charging_stations_sorted = sorted(
                                stations,
                                key=lambda station: station.distance_to(
                                    unserved_customer
                                ),
                            )
                            index = newRoute.route.index(unserved_customer)
                            for station in charging_stations_sorted:
                                newRoute.append_charge_station_at_certain_point(
                                    station, index
                                )
                                if newRoute.is_feasible_all() == True:
                                    solution.remove_w_id_unserved(
                                        unserved_customer
                                    )
                                    solution.served_customers.append(unserved_customer)

                                    solution.routes.append(newRoute)
                                    break
                                else:
                                    newRoute.remove_charge_station_from_route_at_certain_point(
                                        index
                                    )
                                    continue
                        else:
                            solution.remove_w_id_unserved(unserved_customer)
                            solution.served_customers.append(unserved_customer)

                            solution.routes.append(newRoute)

                return solution

        else:
            best_cost = min(costs, key=lambda x: x[0])

            regret_values = []
            for cost, route, customer, route_index in costs:
                regret_values.append(
                    (best_cost[0] - cost, route, customer, route_index)
                )
            # get the 2nd best regret value
            best_regret_customer_sorted = sorted(
                regret_values, key=lambda x: x[0], reverse=True
            )
            k_value = self.k
            if k_value >= len(best_regret_customer_sorted):
                k_value = 1
                if len(best_regret_customer_sorted) == 1:
                    k_value = 0
            to_be_added_route_index = best_regret_customer_sorted[k_value][3]
            solution.routes[
                to_be_added_route_index
            ].route = best_regret_customer_sorted[k_value][1].route
            solution.remove_w_id_unserved(best_regret_customer_sorted[k_value][2])
            solution.served_customers.append(best_regret_customer_sorted[k_value][2])

        return solution
