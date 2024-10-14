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

            if (plant["type"] == "windturbine" and plant['rate'] > 0): 
                plant['pmax'] = round(plant['pmax'] * plant['rate'] / 100,1)
 
            if(self.load > 0 and self.load >= plant['pmin']):
                d['p']    = round( min(plant['pmax'], self.load), 1)
            else:
                d['p'] = 0.0

            ## Subtract assigned load from targeted load 
            print("PLANT: ", d['name'], "LOAD: ", self.load, ", LESS: ",  d['p'])
            self.load -= d['p']

            production_chart.append(d)

        if( self.load > 0 ):
            plant = self._residual_load_adjustment(production_chart)
        
            production_chart.append({plant['name'] : round(self.load,1) })

        
        return production_chart

    def _residual_load_adjustment(self, production_chart):

        list_plants = None
        for p in production_chart:
            if (float(p['p']) == 0):
                list_plants = [ d for d in self.powerplants if (d['name'] == p['name'] ) ]

               # return a plant which has minimum pmin value 
        return sorted(list_plants, key=lambda p: p['pmin'])[0]
