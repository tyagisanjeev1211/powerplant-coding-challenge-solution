class Power_plant:

    """
    This class creates an object for the powerplant with mapping of fuels.

    Note: for % wind, I am using keyword as 'rate', that can be changed.
    """

    def __init__(self, mapping, powerplant):
        self.mapping    = mapping
        self.powerplant = powerplant

    def power_plant(self ):

        for fuel in self.mapping:

           if ( self.powerplant["type"].startswith( fuel ) ):
                if ( "turbojet" in fuel ):
                     self.powerplant["cost"] = self.mapping[ fuel ][ "rate" ]
                     self.powerplant["rate"] = self.mapping[ fuel ][ "rate" ]
                elif ( "euro" in self.mapping[fuel][ "formula" ].lower() ):

                     self.powerplant["cost"] = round( self.mapping[ fuel ][ "rate" ] / self.powerplant["efficiency"], 2)
                     self.powerplant["rate"] = self.mapping[ fuel ][ "rate" ]
                else:
                     self.powerplant["cost"] = 0
                     self.powerplant["rate"] = self.mapping[ fuel ][ "rate" ]

        return self.powerplant


    ##def __repr__(self):

    ##    out = '{ ' + f"""Name       => {self.name}\nType       => {self.type}\nEfficiency => {self.efficiency}\nPmin       => {self.pmin}\nPmax       => {self.pmax}\ncost       => {self.cost}""" + ' }'

    ##    return out
