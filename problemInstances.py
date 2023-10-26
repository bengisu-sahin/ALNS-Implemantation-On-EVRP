import numpy as np

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