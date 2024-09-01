
class Merit_order():
    """
    Powerplants need to produce power based on their efficiency and merit. 
    This class is sorting powerplant objects in merit order  
    """
    def __init__(self, powerplants):
        self.powerplants = powerplants

    def get_merit_order(self):

        ## Sorting based on cost / efficiency 
        return sorted( self.powerplants, key=lambda plant: plant["cost"] )
