from DataObjects.ChargeStation import ChargeStation
from DataObjects.Customer import Customer


class Route:
    def __init__(self, config, depot):
        self.config = config
        self.route = [depot]
        self.depot = depot

    """
    Kısıtlamaları kontrol eder.
    Eğer bir kısıtlama ihlali varsa false döndürür.
    """    

    def is_feasible(self):
        if self.tw_constraint_violated():
            return False
        elif self.payload_capacity_constraint_violated():
            return False
        else:
            return True

    def is_complete(self):
        return self.route[0] == self.depot and self.route[-1] == self.depot and self.depot not in self.route[1:-1]

    # CONSTRAINT VALIDATION METHODS

    """
    "tw_constraint_violated" metodu, zaman penceresi (time window) kısıtlamalarını kontrol eder. Rota üzerindeki her müşterinin zaman penceresi içinde olup olmadığını kontrol eder. Ayrıca şarj istasyonlarına olan enerji eksikliğini ve beklemeyi hesaplar. İhlal durumunda "True" döner, aksi takdirde "False" döner.
    """
    def tw_constraint_violated(self):
        """
        İlk olarak, "elapsed_time" değişkeni başlangıç noktasının hazır olma süresi (ready_time) ve hizmet süresi (service_time) toplamı ile başlatılır. "elapsed_time", rotanın ilk noktasını ziyaret ettikten sonraki geçen süreyi temsil eder.
        """
        elapsed_time = self.route[0].ready_time + self.route[0].service_time #depodan başlıyoruz ilk olarak 0 gelir
        """
        Daha sonra, bir döngü (for döngüsü) başlar. Bu döngü, rota üzerindeki her noktayı sırayla gezerek zaman penceresi kısıtlamalarını kontrol eder. Döngü, rota nesnesinin indekslerini kullanarak çalışır.
        """
        for i in range(1, len(self.route)):
            """
            Her adımda, "elapsed_time" değişkeni, önceki noktadan (route[i - 1]) şu anki noktaya (route[i]) gitmek için geçen süreyi hesaplar. Bu hesaplama, iki nokta arasındaki mesafeyi ("distance_to") hız ile böler ve "elapsed_time" üzerine ekler. Bu, şoförün iki nokta arasında ne kadar süre geçirdiğini hesaplar
            """
            elapsed_time = elapsed_time + self.route[i - 1].distance_to(self.route[i]) / self.config.velocity
            """
            "elapsed_time", şu anki noktanın son teslim tarihi (due_date) ile karşılaştırılır. Eğer "elapsed_time" son teslim tarihini aşarsa, bu, bir zaman penceresi ihlali anlamına gelir ve "True" döner. İhlal varsa, işlem sona erer.
            """
            if elapsed_time > self.route[i].due_date:
                return True
            """
            Eğer "elapsed_time" son teslim tarihini aşmıyorsa, bir başka kontrol yapılır. Eğer şu anki nokta bir şarj istasyonu (ChargeStation) ise, arabanın enerji eksikliği hesaplanır. Bu eksik enerji, mevcut yakıt kapasitesi ile hesaplanan kalan yakıt kapasitesi arasındaki farka dayanır. Ardından, bu eksik enerjiyi şarj etmek için harcanacak süre hesaplanır ve "service_time" olarak atanır.
            """
            if type(self.route[i]) is ChargeStation:
                missing_energy = self.config.tank_capacity - self.calculate_remaining_tank_capacity(self.route[i])
                self.route[i].service_time = missing_energy * self.config.charging_rate
            """
            Şarj istasyonuna harcanan süre ("service_time") ile bekleme süresi ("waiting_time") eklenir. Bekleme süresi, şu anki noktanın hazır olma zamanı ile "elapsed_time" arasındaki farktır. Bu, şoförün belirli bir noktada beklemesi gerektiğinde ne kadar süre beklemesi gerektiğini hesaplar.
            """
            """
            Daha sonra, waiting_time hesaplanır. waiting_time, şoförün şu anki noktaya varmadan önce bekleme yapması gereken süreyi temsil eder. Bu, şoförün belirli bir noktaya ulaşmadan önce o noktanın hazır olma zamanına kadar beklemesi gerekebileceği anlamına gelir. max(self.route[i].ready_time - elapsed_time, 0) ifadesi, bu bekleme süresini hesaplar. self.route[i].ready_time belirli bir noktanın hazır olma zamanını temsil eder. "elapsed_time" ise o ana kadar geçen süreyi temsil eder. Bu ifade, şoförün gerektiği durumda beklemesini sağlar, ancak beklemenin negatif bir değere düşmesini önler (yani, şoför zaten beklemesi gerektiği bir zamanı kaçırmışsa, bekleme süresi sıfır olarak hesaplanır).
            """
            waiting_time = max(self.route[i].ready_time - elapsed_time, 0)
            elapsed_time += waiting_time
            elapsed_time += self.route[i].service_time

        return False
    
    """
    Bu metot, bir rota üzerindeki noktalar arasındaki yakıt tüketimini hesaplar ve yakıt tankının kapasitesini aşılıp aşılmadığını kontrol eder.
    """
    def tank_capacity_constraint_violated(self):
        last = None # Bu değişken, önceki noktanın tutulduğu bir referanstır. Başlangıçta herhangi bir önceki nokta olmadığı için None olarak ayarlanır.
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

    # STATUS CALCULATION METHODS

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