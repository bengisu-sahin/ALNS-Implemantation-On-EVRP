import numpy as np
from DataObjects.ChargeStation import ChargeStation
from DataObjects.Customer import Customer

class RoutingProblemConfiguration:
    """
    Bir rota problemi için yapılandırma bilgilerini içeren sınıf.

    Attributes:
        tank_capacity (float): Araç yakıt tankı kapasitesi.
        payload_capacity (float): Araç taşıma kapasitesi.
        fuel_consumption_rate (float): Yakıt tüketim oranı.
        charging_rate (float): Şarj hızı.
        velocity (float): Ortalama hız.
    """
    def __init__(self, tank_capacity, payload_capacity, fuel_consumption_rate, charging_rate, velocity):
        self.tank_capacity = tank_capacity
        self.payload_capacity = payload_capacity
        self.fuel_consumption_rate = fuel_consumption_rate
        self.charging_rate = charging_rate
        self.velocity = velocity

class RoutingProblemInstance:
    """
    Bir rota problemi örneğini temsil eden sınıf.

    Attributes:
        config (RoutingProblemConfiguration): Örnek için yapılandırma nesnesi.
        depot (Depot): Başlangıç noktasını temsil eden Depot nesnesi.
        customers (list): Müşteri nesnelerinin bulunduğu liste.
        charging_stations (list): Şarj istasyonu nesnelerinin bulunduğu liste.
        cust_cust_dist (numpy.ndarray): Müşteriler arasındaki mesafe matrisi.
        cust_cs_dist (numpy.ndarray): Müşteriler ile şarj istasyonları arasındaki mesafe matrisi.
        vertices (dict): Noktaları ID'leri üzerinden hızlıca bulmak için kullanılan sözlük.
    """
    def __init__(self, config, depot, customers, charging_stations):
        self.config = config
        self.depot = depot
        self.customers = customers
        self.charging_stations = charging_stations

        self.cust_cust_dist = np.zeros((len(self.customers), len(self.customers)))
        self.cust_cs_dist = np.zeros((len(self.customers), len(self.charging_stations)))
        self.vertices = dict()

        # Nokta mesafe matrislerinin başlatılması
        for i in range(0, len(self.customers)):
            for j in range(0, len(self.customers)):
                if i == 0:
                    from_v = self.depot
                else:
                    from_v = self.customers[i-1]

                if j == 0:
                    to_v = self.depot
                else:
                    to_v = self.customers[j-1]

                self.cust_cust_dist[i, j] = from_v.distance_to(to_v)

        for i in range(1, len(self.customers)):
            for j in range(0, len(self.charging_stations)-1):
                if i == 0:
                    from_v = self.depot
                else:
                    from_v = self.customers[i-1]

                self.cust_cs_dist[i, j] = from_v.distance_to(self.charging_stations[j])

        # Nokta bulma sözlüğünün başlatılması
        self.vertices[self.depot.id] = self.depot
        for c in self.customers:
            self.vertices[c.id] = c
        for cs in self.charging_stations:
            self.vertices[cs.id] = cs
            
class Route:
    """
    Rota probleminde bir rotayı temsil eden sınıf.

    Attributes:
        config (RoutingProblemConfiguration): Rota için yapılandırma nesnesi.
        route (list): Rotadaki konumların listesi.
        depot (Depot): Başlangıç ve bitiş noktasını temsil eden Depot nesnesi.
    """
    def __init__(self, config, depot):
        self.config = config
        self.route = [depot]
        self.depot = depot

    def is_feasible(self):
        """Rota uygun mu kontrolü."""
        if self.tw_constraint_violated():
            return False
        elif self.tank_capacity_constraint_violated():
            return False
        elif self.payload_capacity_constraint_violated():
            return False
        else:
            return True

    def is_complete(self):
        """Rota tamamlandı mı kontrolü."""
        return self.route[0] == self.depot and self.route[-1] == self.depot and self.depot not in self.route[1:-1]

    # KISIT KONTROL METODLARI
    def tw_constraint_violated(self):
        """Zaman penceresi kısıtının ihlal edilip edilmediğini kontrol etme."""
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
        """Yakıt kapasitesi kısıtının ihlal edilip edilmediğini kontrol etme."""
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
        """Yük kapasitesi kısıtının ihlal edilip edilmediğini kontrol etme."""
        total_demand = 0
        for t in self.route:
            if type(t) is Customer:
                total_demand += t.demand

        return total_demand > self.config.payload_capacity

    # DURUM HESAPLAMA METODLARI
    def calculate_total_distance(self):
        """Toplam mesafeyi hesaplama."""
        last = None
        dist = 0

        for t in self.route:
            if last is not None:
                dist += last.distance_to(t)
            last = t

        return dist

    def calculate_remaining_tank_capacity(self, until=None):
        """Belirli bir noktaya kadar kalan yakıt kapasitesini hesaplama."""
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
        """Toplam süreyi hesaplama."""
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
        """İlk müşteriye olan mesafeyi hesaplama."""
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
        """İlk müşteriyi alma."""
        if reverse:
            self.route.reverse()

        for t in self.route:
            if type(t) is Customer:
                if reverse:
                    self.route.reverse()
                return t

    def append_route(self, new_route):
        """Başka bir rotayı mevcut rotaya ekleme."""
        if new_route.route[0] == self.depot:
            route_to_append = new_route[1:]

        if self.route[-1] == self.depot:
            self.route = self.route[0:-1]

        self.route = self.route + route_to_append

    def __str__(self):
        """Rota nesnesini stringe dönüştürme."""
        route_str = '['

        for t in self.route:
            route_str += t.id + ', '

        route_str += ']'
        return route_str

    def __repr__(self):
        """Rota nesnesini temsil eden stringi döndürme."""
        route_str = '['

        for t in self.route:
            route_str += t.id + ', '

        route_str += ']'
        return route_str
