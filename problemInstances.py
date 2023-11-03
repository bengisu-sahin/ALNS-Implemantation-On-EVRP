import numpy as np
from DataObjects.ChargeStation import ChargeStation
from DataObjects.Customer import Customer

"""
Bu sınıf veri setinin sonunda yer alan 
    -Q Vehicle fuel tank capacity /194.58/
    -C Vehicle load capacity /1000.0/
    -r fuel consumption rate /1.0/
    -g inverse refueling rate /0.15/  ===>>>>  enerji geri kazanım hızı
    -v average Velocity /1.0/ 
gibi veri setine ait diğer fiziksel özellikleri bir nesnede tutmaya yarayan sınıftır.

!!!!!!! DataSetInformation olarak yazmıştım ancak oradan farklılık olmasına gerek yok diye düşündüm !!!!!
"""
class RoutingProblemConfiguration:
    def __init__(self, tank_capacity, payload_capacity, fuel_consumption_rate, charging_rate, velocity):
        self.tank_capacity = tank_capacity
        self.payload_capacity = payload_capacity
        self.fuel_consumption_rate = fuel_consumption_rate
        self.charging_rate = charging_rate
        self.velocity = velocity

""" 
Bu sınıf problem için gerekli olan instance i oluşturur. Burada config parametresi RoutingProblemConfiguration sınıfının nesnesidir.Veri setine ait fiziksel özellikleri temsil eder. 
"""
class RoutingProblemInstance:
    def __init__(self, config, depot, customers, charging_stations):
        self.config = config
        self.depot = depot
        self.customers = customers
        self.charging_stations = charging_stations

        # distance matrices
        """
        Burada ilki müşteriler arasındaki mesafe 2. si müşteri ve şarj istasyonları arasındaki mesafeyi tutan 2 boyutlu np dizisidir

        """
        self.cust_cust_dist = np.zeros((len(self.customers), len(self.customers)))
        self.cust_cs_dist = np.zeros((len(self.customers), len(self.charging_stations)))

        # vertex lookup dict
        """ 
        her bir noktanın (depo, müşteri , şarj istasyonu) id ile ilişkilendirilen dict yapısı. Bu, daha sonra herhangi bir noktanın id si ile n kolayca erişilebileceğini anlatıyor.
        """
        self.vertices = dict()

        # initialization of distance matrices
        for i in range(0, len(self.customers)):
            for j in range(0, len(self.customers)):

                if i == 0:
                    """ İlk kontrol, döngünün ilk adımında (i = 0) yapılır ve bu durumda from_v değişkenine depo noktası atanır. İlk satırdaki müşteri noktası, depodur ve depo ile kendisi arasındaki mesafeyi temsil eder.
                    """
                    from_v = self.depot
                else:
                    """ 
                    i != 0 ise from_v değişkenine döngünün şu anki müşteri noktasının bir önceki müşteri noktası atanır. Bu, iki müşteri noktası arasındaki mesafeyi hesaplarken bir önceki müşteri noktasını başlangıç noktası olarak kullanır.
                    """
                    from_v = self.customers[i-1]

                if j == 0:
                    to_v = self.depot #depo ile kendisi arasındaki mesafe 0 noktası depoyu temsil eder
                else:
                    """ 
                    j != 0 ise yo_v değişkenine döngünün şu anki müşteri noktasının bir önceki müşteri noktası atanır. Bu, iki müşteri noktası arasındaki mesafeyi hesaplarken bir önceki müşteri noktasını başlangıç noktası olarak kullanır.
                    """
                    to_v = self.customers[j-1]
                """ 
                from_v ve to_v noktaları arasındaki mesafeyi hesaplar ve bu mesafeyi cust_cust_dist matrisinin ilgili hücresine kaydeder. Bu matris 2d dir. Satır ve sütunların kesişim noktasi 2 nokta arasındaki mesafeyi belirler.
                """
                self.cust_cust_dist[i, j] = from_v.distance_to(to_v)

        # müşteri noktaları ile şarj istasyonları arasındaki mesafe matrisi
        for i in range(1, len(self.customers)):
            for j in range(0, len(self.charging_stations)-1):
                if i == 0:
                    from_v = self.depot
                else:
                    from_v = self.customers[i-1]

                self.cust_cs_dist[i, j] = from_v.distance_to(self.charging_stations[j])

        # initialization of the lookup dict
        """ 
        Problemde yer alan tüm noktaları bir sözlükte toplar. Bu sözlük, herhangi bir noktanın benzersiz kimliği üzerinden hızlıca erişilebileceği bir veri yapısı
        """
        self.vertices[self.depot.id] = self.depot
        for c in self.customers:
            self.vertices[c.id] = c
        for cs in self.charging_stations:
            self.vertices[cs.id] = cs
            
class Route:
    def __init__(self, config, depot):
        self.config = config
        self.route = [depot]
        self.depot = depot

    def is_feasible(self):
        if self.tw_constraint_violated():
            return False
        elif self.tank_capacity_constraint_violated():
            return False
        elif self.payload_capacity_constraint_violated():
            return False
        else:
            return True

    def is_complete(self):
        return self.route[0] == self.depot and self.route[-1] == self.depot and self.depot not in self.route[1:-1]

    # CONSTRAINT VALIDATION METHODS
    def tw_constraint_violated(self):
        elapsed_time = self.route[0].ready_time + self.route[0].service_time

        for i in range(1, len(self.route)):
            elapsed_time = elapsed_time + self.route[i - 1].distance_to(self.route[i]) / self.config.velocity

            if elapsed_time > self.route[i].due_date:
                return True

            if type(self.route[i]) is ChargeStation:
                missing_energy = self.config.tank_capacity - self.calculate_remaining_tank_capacity(self.route[i])
                self.route[i].service_time = missing_energy * self.config.charging_rate

            waiting_time = max(self.route[i].ready_time - elapsed_time, 0)
            elapsed_time += waiting_time
            elapsed_time += self.route[i].service_time

        return False

    def tank_capacity_constraint_violated(self):
        last = None
        tank_capacity = self.config.tank_capacity
        for t in self.route:
            if last is not None:
                distance = last.distance_to(t)
                consumption = distance * self.config.fuel_consumption_rate

                tank_capacity -= consumption

                if tank_capacity < 0:
                    return True

                if type(t) is ChargeStation:
                    tank_capacity = self.config.tank_capacity
            last = t

        return False

    def payload_capacity_constraint_violated(self):
        total_demand = 0
        for t in self.route:
            if type(t) is Customer:
                total_demand += t.demand

        return total_demand > self.config.payload_capacity

    # STATUS CALCULATION METHODS
    def calculate_total_distance(self):
        last = None
        dist = 0

        for t in self.route:
            if last is not None:
                dist += last.distance_to(t)
            last = t

        return dist

    def calculate_remaining_tank_capacity(self, until=None):
        last = None
        tank_capacity = self.config.tank_capacity
        for t in self.route:
            if last is not None:
                distance = last.distance_to(t)
                consumption = distance * self.config.fuel_consumption_rate
                tank_capacity -= consumption

                if until == t:
                    return tank_capacity

                if type(t) is ChargeStation:
                    tank_capacity = self.config.tank_capacity

            last = t
        return tank_capacity

    def calculate_total_duration(self):
        elapsed_time = self.route[0].ready_time + self.route[0].service_time

        for i in range(1, len(self.route)):
            elapsed_time = elapsed_time + self.route[i - 1].distance_to(self.route[i]) / self.config.velocity

            if type(self.route[i]) is ChargeStation:
                missing_energy = self.config.tank_capacity - self.calculate_remaining_tank_capacity(self.route[i])
                self.route[i] = missing_energy * self.config.charging_rate

            waiting_time = max(self.route[i].ready_time - elapsed_time, 0)
            elapsed_time += waiting_time
            elapsed_time += self.route[i].service_time

        return elapsed_time

    def calculate_dist_to_first_customer(self, reverse=False):
        dist = 0
        last = None

        if reverse:
            self.route.reverse()

        for t in self.route:
            if last is not None:
                dist += last.distance_to(t)
                if type(t) is Customer:
                    if reverse:
                        self.route.reverse()
                    return dist
            last = t

        return dist

    def get_first_customer(self, reverse=False):
        if reverse:
            self.route.reverse()

        for t in self.route:
            if type(t) is Customer:
                if reverse:
                    self.route.reverse()
                return t

    def append_route(self, new_route):
        if new_route.route[0] == self.depot:
            route_to_append = new_route[1:]

        if self.route[-1] == self.depot:
            self.route = self.route[0:-1]

        self.route = self.route + route_to_append

    def __str__(self):
        route_str = '['

        for t in self.route:
            route_str += t.id + ', '

        route_str += ']'
        return route_str

    def __repr__(self):
        route_str = '['

        for t in self.route:
            route_str += t.id + ', '

        route_str += ']'
        return route_str
