class Production_plan:

    """
    Preparing final production plan  
    """


    def __init__( self, powerplants, load ):
        self.powerplants = powerplants
        self.load        = load

    def get_production_plan(self):

        production_chart = []
        for plant in self.powerplants:
            d = {}
            d['name'] = plant['name']

            if (plant["type"] == "windturbine" and self.load >= plant['pmax']):
                ## wind-turbine with % wind 
                d['p']    = plant['pmax'] * plant['rate'] / 100 if (plant['rate'] > 0) else plant['pmax']
            
            elif(self.load > 0 and self.load > plant['pmin']):
                ## other fuel options 
                d['p']    = min(plant['pmax'], self.load)
            else:
                ## If production target is completed, then other powerplants will have no target to generate power 
                d['p'] = 0.0

            ## Subtract assigned load from targeted load 
            self.load -=  d['p']


            production_chart.append(d)

        return production_chart
