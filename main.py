from initialsolution import initial_solution
from readProblemInstances import readProblemInstances

def getCustomersInfo(customers):
    for customer in customers:
        print(f"Customer ID: {customer.id}")
        print(f"X Coordinate: {customer.x}")
        print(f"Y Coordinate: {customer.y}")
        print(f"Demand: {customer.demand}")
        print(f"Ready Time: {customer.ready_time}")
        print(f"Due Date: {customer.due_date}")
        print(f"Service Time: {customer.service_time}")
        print("---")

def getStationInfo(stations):
    for station in stations:
        print(f"Customer ID: {station.id}")
        print(f"X Coordinate: {station.x}")
        print(f"Y Coordinate: {station.y}")
        print(f"Ready Time: {station.ready_time}")
        print(f"Due Date: {station.due_date}")
        print(f"Service Time: {station.service_time}")
        print("---")

def getDepotInfo(depot):
        print(f"Customer ID: {depot.id}")
        print(f"X Coordinate: {depot.x}")
        print(f"Y Coordinate: {depot.y}")
        print(f"Ready Time: {depot.ready_time}")
        print(f"Due Date: {depot.due_date}")
        print(f"Service Time: {depot.service_time}")
        print("---")  
def getConfig(config): 
        print(f"Tank Capacity: {config.tank_capacity}")
        print(f"Payload Capacity: {config.payload_capacity}")
        print(f"Fuel Consumption Rate: {config.fuel_consumption_rate}")
        print(f"Charging Rate: {config.charging_rate}")
        print(f"Velocity: {config.velocity}")           
        print("---")

def main(): 
    problemFile = readProblemInstances('SchneiderData/c103_21.txt')  # Değişken atama işlemi düzeltilmiş ve parantez eklendi.
    getCustomersInfo(problemFile.customers)
    initial_solution(problemFile.depot,problemFile.customers,problemFile)
    #getStationInfo(problemFile.charging_stations)
    #getDepotInfo(problemFile.depot)
    #getConfig(problemFile.config)


if __name__ == "__main__":
    main()