import os
from DataObjects.ChargeStation import ChargeStation
from DataObjects.Customer import Customer
from DataObjects.Target import Target
from problemInstances import RoutingProblemConfiguration, RoutingProblemInstance

def readProblemInstances(file):
    """
    Verilen dosyadan rota problemi örneklerini okuyan fonksiyon.

    Args:
        file (str): Okunacak dosyanın adı.

    Returns:
        RoutingProblemInstance: Okunan rota problemi örneği.
    """
    with open(file) as f:
        f.readline()  # başlık satırını atla

        target_line = f.readline()

        customers = []
        fuel_stations = []
        depot = None

        while target_line != '\n':
            stl = target_line.split()  # bölünmüş target_line
            idx = int(stl[0][1:])

            if stl[1] == 'd':
                depot = Target(stl[0], idx, int(float(stl[2])), int(float(stl[3])), int(float(stl[5])),
                            int(float(stl[6])), int(float(stl[7])))
            elif stl[1] == 'f':
                new_target = ChargeStation(stl[0], idx, int(float(stl[2])), int(float(stl[3])), int(float(stl[5])),
                                            int(float(stl[6])), int(float(stl[7])))
                fuel_stations.append(new_target)
            elif stl[1] == 'c':
                new_target = Customer(stl[0], idx, int(float(stl[2])), int(float(stl[3])), int(float(stl[4])),
                                    int(float(stl[5])), int(float(stl[6])), int(float(stl[7])))
                customers.append(new_target)

            target_line = f.readline()

        configuration_line = f.readline()
        tank_capacity = float(configuration_line.split('/')[1])  # q Vehicle fuel tank capacity

        configuration_line = f.readline()
        load_capacity = float(configuration_line.split('/')[1])  # C Vehicle load capacity

        configuration_line = f.readline()
        fuel_consumption_rate = float(configuration_line.split('/')[1])  # r fuel consumption rate

        configuration_line = f.readline()
        charging_rate = float(configuration_line.split('/')[1])  # g inverse refueling rate

        configuration_line = f.readline()
        velocity = float(configuration_line.split('/')[1])  # v average Velocity
        fileName = os.path.splitext(os.path.basename(file))[0]
        return RoutingProblemInstance(RoutingProblemConfiguration(tank_capacity, load_capacity, fuel_consumption_rate,
                                                                charging_rate, velocity), depot, customers,fuel_stations,fileName)