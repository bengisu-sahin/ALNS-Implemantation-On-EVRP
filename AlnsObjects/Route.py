from DataObjects.ChargeStation import ChargeStation
from DataObjects.Customer import Customer
import matplotlib.pyplot as plt

class Route:
    """
    Represents a route in the EVRP problem.
    """

    def __init__(self, config, depot):
        """
        Initializes a Route object.

        Args:
            config (Config): The configuration object containing the parameters for the EVRP problem.
            depot (Node): The depot node where the route starts and ends.
        """
        e = 0.8
        p = 1.2041
        g = 9.81
        Cd = 0.4
        Cr = 0.015
        A = 7
        self.config = config
        self.route = [depot]
        self.depot = depot
        self.alpha = (0.5 * Cd * p * A * (self.config.velocity ** 3)) / (1000 * e)
        self.beta = (g * Cr * self.config.velocity) / (1000 * e)

    def is_feasible(self):
        """
        Checks if the route satisfies all the constraints.

        Returns:
            bool: True if the route is feasible, False otherwise.
        """
        if self.tw_constraint_violated():
            return False
        elif self.payload_capacity_constraint_violated():
            return False
        else:
            return True

    def is_feasible_all(self):
        """
        Checks if the route satisfies all the constraints, including the tank capacity constraint.

        Returns:
            bool: True if the route is feasible, False otherwise.
        """
        if self.tw_constraint_violated():
            return False
        elif self.tank_capacity_constraint_violated():
            return False
        elif self.payload_capacity_constraint_violated():
            return False
        else:
            return True

    def is_complete(self):
        """
        Checks if the route is complete, i.e., it starts and ends at the depot and the depot is not visited in between.

        Returns:
            bool: True if the route is complete, False otherwise.
        """
        return self.route[0] == self.depot and self.route[-1] == self.depot and self.depot not in self.route[1:-1]

    def tw_constraint_violated(self):
        """
        Checks if the time window constraints are violated in the route.

        Returns:
            bool: True if the time window constraints are violated, False otherwise.
        """
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

    def node_count_in_route(self):
        """
        Returns the number of nodes in the route.

        Returns:
            int: The number of nodes in the route.
        """
        return len(self.route)

    def tank_capacity_constraint_violated(self):
        """
        Checks if the tank capacity constraint is violated in the route.

        Returns:
            bool: True if the tank capacity constraint is violated, False otherwise.
        """
        last = None
        tank_capacity = self.config.tank_capacity
        for t in self.route: #Döngü, rota üzerindeki her bir noktayı sırayla gezerek yakıt tüketimini ve yakıt kapasitesini kontrol eder.
            if last is not None:
                distance = last.distance_to(t) #Her adımda, last değişkeni kullanılarak önceki noktadan şu anki noktaya giden mesafe hesaplanır ve "distance" değişkenine atanır.
                consumption = distance * self.config.fuel_consumption_rate #"consumption" değişkeni hesaplanır. Bu değişken, "distance" ile yakıt tüketim oranı ("fuel_consumption_rate") çarpılarak hesaplanır. Bu, şoförün bu mesafeyi kat etmek için ne kadar yakıt tükettiğini temsil eder.

                tank_capacity -= consumption #Kalan tank kapasitesi hesaplanır/arabanın o noktaya ulaşırken kalan yakıt kapasitesini hesaplar.

                """
                "tank_capacity" değeri negatifse, bu, yakıt tankının kapasitesini aştığı anlamına gelir ve bir kısıtlama ihlali vardır. Bu durumda, metot "True" döner ve kısıtlama ihlali olduğu bildirilir.
                """
                if tank_capacity < 0: #
                    return True  
                """
                Eğer şu anki nokta bir şarj istasyonu (ChargeStation) ise, şoförün yakıtı şarj ettiği ve yakıt kapasitesinin yenilendiği kabul edilir. Bu nedenle, "tank_capacity" tekrar maksimum yakıt kapasitesine (self.config.tank_capacity) ayarlanır.
                """
                if type(t) is ChargeStation:
                    tank_capacity = self.config.tank_capacity
                  

            last = t #En son olarak, "last" değişkeni güncellenir ve bir sonraki noktaya geçilir. Bu, döngünün bir sonraki adımında önceki noktanın şu anki nokta olması için gereklidir.

        return False #Döngü tamamlandığında, tüm noktalar için yakıt tüketimi ve yakıt kapasitesi kontrol edilmiştir. Eğer hiçbir noktada yakıt kapasitesi aşılmamışsa, metot "False" döner ve yakıt kapasitesi kısıtlamalarına uyulur.


    def calculate_time_between_nodes(self, from_node, to_node):
        """
                İki düğüm arasında seyahat etmek için geçen süreyi hesaplar.

                Args:
                    from_node (Node): Başlangıç düğümü.
                    to_node (Node): Hedef düğüm.

                Returns:
                    float: İki düğüm arasında seyahat etmek için geçen süre.
        """
        return from_node.distance_to(to_node) / self.config.velocity
    
    def payload_capacity_constraint_violated(self):
        total_demand = 0 #İlk olarak, "total_demand" adında bir değişken başlatılır ve başlangıçta sıfır (0) değeri ile başlar. Bu değişken, rota üzerindeki müşterilerin toplam taleplerini tutar.
        for t in self.route: #Bir döngü, rota üzerindeki her bir noktayı sırayla gezerek çalışır.
            """
            Döngünün her adımında, "t" adlı bir nokta (müşteri veya diğer nokta) ele alınır ve tipi kontrol edilir (type(t)). Eğer "t" bir müşteriyse (Customer), o müşterinin talebi (demand) "total_demand" değişkenine eklenir.
            Döngü tamamlandığında, "total_demand", rota üzerindeki müşterilerin toplam talebini temsil eder.
            """
            if type(t) is Customer: 
                total_demand += t.demand
        """
        Son olarak, "total_demand" ile aracın taşıma kapasitesi (self.config.payload_capacity) karşılaştırılır. Eğer toplam talep, aracın taşıma kapasitesini aşıyorsa, bu bir kısıtlama ihlali anlamına gelir ve metot "True" döner. Yani, aracın taşıma kapasitesi kısıtlamalarına uyulmamıştır.
        """
        return total_demand > self.config.payload_capacity

    def get_last_customer(self):
        for t in reversed(self.route):
            if type(t) is Customer:
                return t
    def get_last_object(self):
        return self.route[-1]
    # STATUS CALCULATION METHODS
    def calculate_load_carried_until_customer(self, customer):
        """
        Bu metot, bir müşteriye kadar olan toplam yükü hesaplamak için kullanılır. Bu yük, müşteriye kadar olan tüm müşterilerin taleplerinin toplamıdır.
        """
        total_demand = 0
        for t in self.route:
            if t == customer:
                break
            if type(t) is Customer:
                total_demand += t.demand

        return total_demand

    """
    Bu metodun temel amacı, bir rota üzerindeki toplam mesafeyi hesaplamaktır. Bu mesafe, belirli bir rotayı oluşturan noktalar arasındaki toplam yolculuk mesafesini verir.
    """
    def calculate_total_distance(self):
        last = None
        dist = 0

        for t in self.route:
            if last is not None:
                dist += last.distance_to(t)
            last = t

        return dist

    """
    Bu kod parçası, rota üzerindeki belirli bir noktaya kadar olan kalan yakıt kapasitesini hesaplayan "calculate_remaining_tank_capacity" adlı bir metodu içerir. Bu metot, şoförün belirli bir noktaya ulaşmak için ne kadar yakıt kapasitesine ihtiyacı olduğunu hesaplar ve bu kapasitenin ne kadarının kaldığını kontrol eder
    """
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

    """
    Bu kod parçası, bir rota üzerindeki toplam süreyi (duration) hesaplayan "calculate_total_duration" adlı bir metodu içerir. Bu metot, rota üzerindeki her bir noktanın hizmet süresi, yolculuk süresi ve bekleme süresi dahil olmak üzere toplam süreyi hesaplar. 
    """
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

    """
    Bu metot, "calculate_dist_to_first_customer", rotada bulunan ilk müşteriye olan mesafeyi hesaplamak için kullanılır. ?
    """
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

    """
    Bu metot, bir rota üzerindeki ilk müşteriyi (Customer) bulmak için kullanılır. 
    """
    def get_first_customer(self, reverse=False):
        if reverse:
            self.route.reverse()

        for t in self.route:
            if type(t) is Customer:
                if reverse:
                    self.route.reverse()
                return t
    def get_charge_stations(self):
        return [t for t in self.route if type(t) is ChargeStation]

    def get_customers(self):
        return [t for t in self.route if type(t) is Customer]

    def remove_customer_from_route(self, customer):
        self.route.remove(customer)

    def remove_charge_station_from_route(self, charge_station):
        self.route.remove(charge_station)

    def remove_charge_station_from_route_at_certain_point(self, index):
        self.route.pop(index)

    def find_item_index_in_solution(self, item):
        # Müşteriyi çözüm içinde ara ve indeksini bul
        for i in range(len(self.route)):
            if self.route[i] == item:
                return i

    def calculate_energy_consumption(self,from_node,to_node):
        #TODO: Implement this method
        
        return (self.alpha*1+self.beta*(self.calculate_load_carried_until_customer(to_node)+3000))*self.calculate_time_between_nodes(from_node,to_node)

    def calculate_obj_function(self):
        #TODO: Implement this method
        route_length = len(self.route)
        total_energy_used = 0
        for i in range(route_length - 1):
            from_node = self.route[i]
            to_node = self.route[i + 1]
            total_energy_used += self.calculate_energy_consumption(from_node, to_node)

        return total_energy_used
    
    def appendcustomer_at_certain_point(self, customer, index):
        self.route.insert(index, customer)

    def append_charge_station_at_certain_point(self, charge_station, index):
        self.route.insert(index, charge_station)

    def remove_charge_station_from_route_by_index(self, index):
        self.route.remove(self.route[index])

    """
    Sonuç olarak, bu metot, "self" nesnesi ile "new_route" nesnesini birleştirerek yeni bir rota oluşturur. Bu, lojistik ve taşıma problemleri gibi alanlarda, farklı rotaları birleştirerek daha etkili ve optimize edilmiş rota planlaması yapmak için kullanışlı
    """
    def append_route(self, new_route):
        if new_route.route[0] == self.depot:
            route_to_append = new_route[1:]

        if self.route[-1] == self.depot:
            self.route = self.route[0:-1]

        self.route = self.route + route_to_append

    #ROTAYI YAZDIRMA FONKSİYONLARI
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
    
    """
    Tüm rotaları tek bir grafikte görselleştirmek için kullanılır.
    """
    def visualizeAllRoutes(self):
        coordinates=[]
        rotaC=[]
        depot=[]
        for route in self.route:
            for location in route.route:
                coord=[]
                coord.append(location.x)
                coord.append(location.y)
                coordinates.append(coord)
            rotaC.append(coordinates)
            coordinates=[]
        print(rotaC)

        # Bir figure oluşturun
        # Grafik boyutunu ayarla
        fig, ax = plt.subplots(figsize=(10, 8))  # Genişlik: 10 birim, Yükseklik: 8 birim

        for route in rotaC:
            x, y = zip(*route)
            ax.plot(x, y, marker='o', linestyle='-')

            # Depot noktasına daire eklemek
            depot_x, depot_y = route[0]
            ax.plot(depot_x, depot_y, marker='o', markersize=10, markeredgecolor='r', markerfacecolor='none')

        # [40, 50] noktasına bir işaret eklemek
        ax.annotate('[40, 50]', (40, 50), textcoords="offset points", xytext=(0, 10), ha='center')

        # Eksenlerin kesişimi 0,0 olacak şekilde düzenleme
        ax.spines['left'].set_position('zero')
        ax.spines['bottom'].set_position('zero')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')

        # Eksenlerdeki noktaların yerleşimini ayarlama
        ax.xaxis.set_major_locator(plt.MultipleLocator(5))
        ax.yaxis.set_major_locator(plt.MultipleLocator(5))

        ax.set_xlabel('X Koordinatı')
        ax.set_ylabel('Y Koordinatı')
        ax.set_title('Tüm Rotaların Birleştirilmiş Grafiği')

        ax.grid(True)
        plt.show()

    """
    Her bir rotayı ayrı ayrı görselleştirmek için kullanılır.
    """
    def visualizeRoute(self):
        depot_x = 0
        depot_y = 0
        id = 1
        for route in self.route:
            fig, ax = plt.subplots(figsize=(10, 8))
            x_points = []
            y_points = []
            labels = []
            content = []
            for location in route.route:
                x, y = location.x, location.y
                label = f'{location.id}({x}, {y})'  # Display location ID with coordinates
                x_points.append(x)
                y_points.append(y)
                labels.append(location.id)  # Display only location ID
                content.append(label)

            # Determine the marker style based on the location type
            markers = ['o' if isinstance(location, Customer) else 's' if isinstance(location, ChargeStation) else 'D' for location in route.route]

            # Connect the points with lines
            ax.plot(x_points, y_points, '-b', marker='o', markersize=8, markerfacecolor='blue', label='Customers')

            # Plot charge stations with a different marker
            charge_station_indices = [i for i, location in enumerate(route.route) if isinstance(location, ChargeStation)]
            charge_station_x = [x_points[i] for i in charge_station_indices]
            charge_station_y = [y_points[i] for i in charge_station_indices]
            ax.plot(charge_station_x, charge_station_y, 'rs', label='Charge Stations')

            # Plot depot locations (D0) with a different marker
            depot_indices = [i for i, location in enumerate(route.route) if location.id == 'D0']
            depot_x = [x_points[i] for i in depot_indices]
            depot_y = [y_points[i] for i in depot_indices]
            ax.plot(depot_x, depot_y, 'gD', markersize=8, markerfacecolor='green', label='Depot (D0)')

            # Annotate each point with its label
            for x, y, label in zip(x_points, y_points, labels):
                ax.annotate(label, (x, y), textcoords="offset points", xytext=(0, 10), ha='center')

            ax.set_xlabel('X-axis')
            ax.set_ylabel('Y-axis')
            ax.set_title(f'Route Visualization - Route {id}')
            ax.legend()

            plt.annotate(', '.join(content), xy=(0.5, -0.12), xycoords='axes fraction', fontsize=12, ha='center')

            id += 1
            plt.show()

    def number_of_customers(self):
        """
        Returns the number of customers in the route.

        Returns:
            int: The number of customers in the route.
        """
        return len(self.get_customers())
    
    def number_of_charge_stations(self):
        """
        Returns the number of charge stations in the route.

        Returns:
            int: The number of charge stations in the route.
        """
        return len(self.get_charge_stations())

