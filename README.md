# Solution of powerplant-coding-challenge

### Summary in points 

- A power production plan needs to be prepared.
- This solution must be developed as RestAPI, which needs to be built with an endpoint "/productionplan" that accepts a POST request.
- The body of this POST request will be a payload JSON file.
- The cost of generating power can be different for every powerplant and is dependent on external factors.
	- The cost of producing power using a turbojet that runs on kerosine is higher compared to the cost of generating power using a gas-fired powerplant because gas is cheaper compared to kerosine and because the thermal efficiency of a gas-fired powerplant is around 50% (2 units of gas will generate 1 unit of electricity), while that of a turbojet is only around 30%.
	- The cost of generating power using windmills, however, is zero. Thus, deciding which powerplants to activate is dependent on the merit order.
	
### payload
contains three type of data 
**load**: Load is the demand of power in an hour. The load is the amount of energy (MWh) that needs to be generated. At any moment in time, all available powerplants need to generate the power to exactly match the load.
**fuels**: There are three types of fuels mentioned in JSON.
	- Gas: the price of gas per MWh. Thus, if gas is at 6 euros/MWh and if the efficiency of the powerplant is 50% (i.e., 2 units of gas will generate one unit of electricity), the cost of generating 1 MWh is 12 euros.
	- Kerosin: the price of kerosine per MWh
	- wind: Percentage of wind. Example: if there is on average 25% wind during an hour, a wind turbine with a Pmax of 4 MW will generate 1 MWh of energy.
	- CO2: (This was optional, and I have a small confusion about using this variable.) so I have not included this in the solution)
**Powerplants**: 
	- name: Name of Powerplant
	- type: type of energy used in a plant to generate power
	- Efficiency: at which they convert a MWh of fuel into a MWh of electrical energy. Wind turbines do not consume 'fuel' and thus are considered to generate power at zero price.
	- PMIN: the minimum amount of power the powerplant generates when switched on
	- pmax: the maximum amount of power the powerplant can generate
  
## Assumptions 
- **1**: If a residual load after wind turbine production is less than the PMIN value of gasfired and greater than the pmax value of turbojet, then a plant with smaller 'PMIN' will be selected to cater remaining power requirement. 
- **2**: Final demand will not be more than total power capacity of all plants.
  
**modules** I have developed four modules for this solution: 
- **fuel_mapping.py** : Class Fuel_mapping. This class read the fuels section of the payload and filter for fuel type with a formula and its rate.  
- **powerplant.py** : Class Power_plant. This class reads the powerplants section of the payload and generates an object of powerplants with its fuel mapping object.
                      After this class, we have every required information in the powerplant object, and this object is ready for processing.
- **merit_order.py** : Class Merit_order. This class sorts the list of powerplant objects based on power generation cost.
- **Merit_order** : Class Production_plan. This class prepares the actual power production plan based on a sorted list of powerplant objects. 

**Note:** I am handing post request directly using Request class 
```
async def productionplan(request: Request):
```
So, 
```
http://127.0.0.1:8888/docs
``` 
will give "Parameters" as "No parameters" 

**Python version** 
```
[styagi@be69001a324d src]$ python3 --version
Python 3.11.9
```

**requirements.txt**
```
[styagi@be69001a324d src]$ cat requirements.txt
aiofiles==24.1.0
annotated-types==0.7.0
anyio==4.4.0
click==8.1.7
fastapi==0.112.2
h11==0.14.0
idna==3.8
pydantic==2.8.2
pydantic_core==2.20.1
python-multipart==0.0.9
sniffio==1.3.1
starlette==0.38.2
typing_extensions==4.12.2
uvicorn==0.30.6
```

**Dockerfile** I am using RHEL8 Base image to develop solution 
```
FROM redhat/ubi8

LABEL "Developed by"="Sanjeev Tyagi"
LABEL "medium.com"="https://medium.com/@tyagisanjeev1211"

## Change password with your convenience
RUN echo 'root:q48stG1a' |chpasswd

## RUN dnf upgrade
RUN dnf -y install python3.11
RUN dnf -y install python3.11-pip
RUN pip3 install fastapi
RUN pip3 install uvicorn            ## Web server 
RUN pip3 install aiofiles           ## Static file (javascript, css, media files 
RUN pip3 install python-multipart   ## multipart HTML form. Like file upload 

RUN useradd styagi
RUN echo 'styagi:docker123' | chpasswd

RUN mkdir -p /home/styagi/app
ADD project /home/styagi/app/
RUN chown -R styagi:styagi /home/styagi

EXPOSE 8888

USER styagi 

WORKDIR /home/styagi/app/src/

CMD nohup python3 main.py 
```


**Deply the solution** 
- Git clone to local 
```
git clone https://github.com/tyagisanjeev1211/angleClockHands.git
```

- Directory change to app folder and check permissions 
```
cd /home/styagi/src/
```

- Build Docker image 
```
docker build -t powerplant-coding-challenge-image . 
```

- If there is no error in building then, list images  
```
docker images 
```

- Creating a container. Option -p to publish a port for container: there was a requirement there API must be exposed on port 8888.  
```
docker run -d --name powerplant-coding-container -p 8888:8888 powerplant-coding-challenge-image
```

- List of running containers 
```
docker ps -a 
```

- check whether localhost on port 8888 is reachable or not 
```
curl -v http://127.0.0.1:8888 
```

- Execute curl command to get response 
```
curl -i -X POST -H "Content-Type:application/json" -d @payload3.json http://127.0.0.1:8888/productionplan
``` 
