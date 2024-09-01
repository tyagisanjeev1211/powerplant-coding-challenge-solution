from fastapi import FastAPI, Request

from fastapi.encoders  import jsonable_encoder
from fastapi.responses import JSONResponse

import uvicorn 

from production_plan import Production_plan
from merit_order     import Merit_order
from powerplant      import Power_plant
from fuel_mapping    import Fuel_mapping

app = FastAPI(
    title="powerplant-coding-challenge",
    description="""Power / Energy production plan for different powerplants need to produce. Load is given and taking into account the cost of the underlying energy sources (gas, kerosine) and the Pmin and Pmax of each powerplant.""",
)


@app.post("/productionplan", response_class=JSONResponse)
async def productionplan(request: Request):
    """
       path /productionplan will get the request in JSON format. 
       
       Need to update: 
           - Exception handling
           - Logging 
    """

    ## Payload from request 
    payload = await request.json()

    ## Mapping of payload's fuels section with powerplants section
    mapping    = Fuel_mapping(payload).fuel_mapping()

    ## Creating powerplant objects with information of fuel mapping config 
    powerplants = []
    for powerplant in payload["powerplants"]:
       
       powerplants.append( Power_plant( mapping, powerplant ).power_plant() )


    ## Rearranging powerplant objects in order of merit of cost and efficiency 
    powerplants      = Merit_order( powerplants ).get_merit_order()
    
    ## Now, Creating produciton plan 
    production_chart = Production_plan( powerplants, payload["load"] ).get_production_plan()    

    ## Response of request in json format
    return JSONResponse(content=jsonable_encoder( production_chart ))


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8888)


