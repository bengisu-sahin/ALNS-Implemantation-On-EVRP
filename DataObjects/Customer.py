import math as m
from DataObjects.Target import Target

""" 
Bu sınıf veri setinde StringID değerleri "C" olan verileri içermektedir. Bunlar müşteri düğümlerini temsil eder.
Target Sınıfından farklı olarak müşterilerin talep ettikleri yük miktarını (demand) de sınıf özelliği olarak içerir.
"""

class Customer(Target):
    def __init__(self, id, idx, x, y, demand, ready_time, due_date, service_time):
        super(Customer, self).__init__(id, idx, x, y, ready_time, due_date, service_time)
        self.demand = demand

    def getCustomer(self):
        return self
