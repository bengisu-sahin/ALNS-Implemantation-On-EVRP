from AlnsOperators.CustomerOperators import Regret_K_Insertion, greedyCustomerInsertionOperator, leastTimeWindowCustomerRemovalOperator, relatedCustomerRemovalOperator, removeRandomCustomerOperator, worstDistanceCustomerRemovalOperator
from AlnsOperators.RouteOperators import greedyRouteRemovalOperator, randomRouteRemovalOperator
from AlnsOperators.StationOperators import Compare_K_Insertion, bestStationInsertionOperator, randomStationRemovalOperator, worstChargeUsageStationRemovalOperator, worstStationRemovalOperator


class ALNS ():
    def __init__(self, bestSolution, currentSolution ):
        self.bestSolution = bestSolution
        self.currentSolution = currentSolution

        # Customer removal operators
        self.relatedCustomerOp=relatedCustomerRemovalOperator()
        self.removeRandomCustomerOp=removeRandomCustomerOperator()
        self.leastTimeWindowCustomerRemovalOp=leastTimeWindowCustomerRemovalOperator()
        self.worstDistanceCustomerRemovalOp=worstDistanceCustomerRemovalOperator()
        self.customerRemovalOps=[self.relatedCustomerOp,self.removeRandomCustomerOp,self.leastTimeWindowCustomerRemovalOp,self.worstDistanceCustomerRemovalOp]

        # Customer insertion operators
        self.greedyCustomerInsertionOp=greedyCustomerInsertionOperator()
        self.Regret_K_InsertionOp=Regret_K_Insertion(k=2)
        self.customerInsertionOps=[self.greedyCustomerInsertionOp,self.Regret_K_InsertionOp]

        #CHARGE STATION REMOVAL OPERATORS
        self.randomStationRemovalOp=randomStationRemovalOperator()
        self.worstChargeUsageStationRemovalOp=worstChargeUsageStationRemovalOperator()      
        self.worstStationRemovalOp=worstStationRemovalOperator()
        self.stationRemovalOps=[self.randomStationRemovalOp,self.worstChargeUsageStationRemovalOp,self.worstStationRemovalOp]

        #CHARGE STATION INSERTION OPERATORS
        self.bestStationInsertionOp=bestStationInsertionOperator()
        self.Compare_K_InsertionOp=Compare_K_Insertion(k=2)
        self.stationInsertionOps=[self.bestStationInsertionOp,self.Compare_K_InsertionOp]

        # Route removal operators
        self.randomRouteRemovalOp=randomRouteRemovalOperator()
        self.greedyRouteRemovalOp=greedyRouteRemovalOperator()
        self.routeRemovalOps=[self.randomRouteRemovalOp,self.greedyRouteRemovalOp]
        

