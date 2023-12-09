import math as m

"""
Bu sınıf Schneider veri setlerindeki her bir satır veriyi temsil eder.
Bu veri setindeki StringID, Type, x, y, demand, ReadyTime, DueDate, ServiceTime sütunlarını sınıf özellikleri olarak içerir.
Ek olarak konum bilgisini döndüren bir fonksiyon ve nesnenin özelliklerini döndüren bir fonksiyon içerir.
Aynı zamanda iki hedef arasındaki mesafeyi hesaplayan bir 'distance_to' fonksiyonu da içerir.
"""

class Target:
    def __init__(self, id, idx, x, y, ready_time, due_date, service_time):
        self.id = id
        self.idx = idx
        self.x = x
        self.y = y
        self.ready_time = ready_time
        self.due_date = due_date
        self.service_time = service_time

    def distance_to(self, compared_target):
        return m.sqrt((self.x - compared_target.x) ** 2 + (self.y - compared_target.y) ** 2)
    def distance_to_avg_of_two(self, compared_target1, compared_target2):
        return m.sqrt((self.x - (compared_target1.x+compared_target2.x)/2) ** 2 + (self.y - (compared_target1.y+compared_target2.y)/2) ** 2)
        

    def get_coordinates(self):
        return self.x, self.y

    def __str__(self):
        return "type: {0}, id: {1}, x: {2}, y: {3}".format(type(self), self.id, self.x, self.y)