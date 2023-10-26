from DataObjects.Target import Target

""" 
Bu sınıf veri setinde StringID değerleri "S" olan verileri içermektedir. Bunlar istasyonları temsil eder.
"""
class ChargeStation(Target):
    def __init__(self, id, idx, x, y, ready_time, due_date, service_time):
        super(ChargeStation, self).__init__(id, idx, x, y, ready_time, due_date, service_time)