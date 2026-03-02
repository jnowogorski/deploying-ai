# Assignment 2: Chat app related to Air Quality measurements and effects of Air Quality on Health 

### What can be discussed:

- When asked, chat will provide current Air Quality readings for given city by making API calls to https://api.waqi.info service.  
The answer is rephrased  by the model when provided to the user in chat.  
Please see details below in `Service 1`.

- It will provide answers to questions related to Air Quality and health.  
The questions are resolved via semantic search of the `Guide to Air Quality and Health` PDF document.  
Please see details below in `Service 2`.  

- It will also provide (simulated) readings of the air temperature and humidity in the house for given room.  
The readings are obtained via MCP Connection as described in `Service 3`.  
       
## Example questions:
- What is air quality in Toronto? ->  this question should use of `Service 1`
- Is poor air quality bad for humans? -> this question should use `Service 2`
- What is temperature in Bedroom? -> this question should use `Service 3`


## Services:

This implementation is based on LangGraph's tools. 
The file main.py contains the llm model calls that controls the chat.  
Tools are in the files tools_*.py. in respective  folder: `./service_1`, `./service_2`, `./service_3`.


### Service 1: API Calls

+ This service gets Air Quality readings for a given city by making API calls to https://api.waqi.info/feed/:city/?token=:token service.  
It takes location  parameter `city` and query parameter `token`.  
The related website for air quality pollution is: https://aqicn.org/.
The `.secrets` file must have: `ASSIGNMENT_2__SERVICE_1__WORLD_AIR_QUALITY_INDEX_API_KEY=<key>`  
The key can be obtained here: https://aqicn.org/data-platform/token/   
(Please contact me privately if you can't generate key.)

+ Pollutants measurements:

    - PM2.5
    - PM10
    - Ozone (O₃)
    - Nitrogen dioxide (NO₂)
    - Sulfur dioxide (SO₂)
    - Carbon monoxide (CO)

+ Meteorological measurements:

    - Dew point temperature
    - Relative humidity
    - Atmospheric pressure
    - Air temperature
    - Wind speed
    - Wind gust speed


### Service 2: Semantic Query

+ Semantic Query of the `Guide to Air Quality and Health` PDF document.  
File location: https://www.airnow.gov/sites/default/files/2018-04/aqi_brochure_02_14_0.pdf  
This original PDF file is also provided in the `./service_2/data` folder.  
The embeddings are provided in local ChromaDB instance with persistence  provided in `./service_2/data/chroma_db`.

+ Preperation was done by running cells in the file `./service_2/chromadb_fill_embeddings.ipynb`:

    - Downloads `Guide to Air Quality and Health` from the internet, 
    - Splits file into chunks,
    - Creates embeddings,
    - Fills embeddings into persistent ChromaDB instance located in `./service_2/data/chroma_db`

+ Testing vector db was done by running cells in file `./service_2/chromadb_test_semantic_query.ipynb` was used to test local vector db created above.

### Service 3: MCP Server Connection

+ This service has `MCP client` that makes a connection to the MCP server.  
The server is accessed via my `ngrok` url configured in the `.env` file.  
The `.env` file has `ASSIGNMENT_2__SERVICE_3__MCP_CLIENT_URL=<link>`.  
Please let me know if you have issues accessing my mcp server.


+ `MCP server` currently only provides `simulated randomized` values for rooms but my intention is to eventually make it read values from actual home air quality sensors.    
The MCP server code is located in `./service_3/service_3_air_in_room_mcp_server.py` file is running on my Raspberry Pi.  
On my RPi server runs with domain value `ASSIGNMENT_2__SERVICE_3__MCP_SERVER_DOMAIN=<domain>` from the `.env` file.  

+ Home air measurements:

    - Air temperature
    - Relative humidity

+ Home air measurements - Future plan: is to read real values and also read radon & other pollutants):

    - Connect to actual sensor `Airthings 2960 View Plus` that reads Radon & Air Quality (PM, CO2, VOC, Humidity, Temp, Pressure).
    - The manufacturer of this sensor provides cloud API to which I will (future) connect from within the MCP server.  
        

## User Interface

+ Added conversational style.
+ Implemented in Gradio

---

## Guardrails and Other Limitations

* Included guardrails that prevent users from:

  * Accessing or revealing the system prompt.
  * Modifying the system prompt directly.

* The model should not respond to questions on certain restricted topics:

  * Cats or dogs
  * Horoscopes or Zodiac Signs
  * Taylor Swift

