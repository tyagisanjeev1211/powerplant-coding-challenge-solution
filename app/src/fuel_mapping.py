import re

class Fuel_mapping:

    """
    The payload's fuels section and the powerplants section have different names, 
    Like: fuels section have name kerosine and powerplants section have type for kerosine is turbojet 
    Thus, mapping of the fuel information is required.
    """

    def __init__(self, payload):
        self.payload = payload

    def fuel_mapping(self):
        mapping = {}
        for fuel, rate in self.payload["fuels"].items():

            ## Matching alphabets before brackets start
            ## Something like "gas(euro/MWh)"; here I am capturing the word gas only as group p 
            match_obj = re.match("(\w+)\((.*)\)", fuel, re.I)

            fuel = match_obj.group(1)

            if (fuel == "kerosine" ):
                mapping[ "turbojet" ] = { "formula" : match_obj.group(2), "rate" : rate }
            else:
                mapping[ match_obj.group(1) ] = { "formula" : match_obj.group(2), "rate" : rate }

        return mapping

