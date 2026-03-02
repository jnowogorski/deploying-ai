# Assignemnt2 - Service 1: API Calls
# Get 'city air quality' data from the 'World Air Quality Index Project'
from langchain.tools import tool
from dotenv import load_dotenv
import requests
import os

from assignment_chat.service_1.city_air_quality_response import AirQualityResponse, AirQualityData
from assignment_chat.service_1.city_air_quality_summary import build_air_quality_summary

load_dotenv(".env")
load_dotenv(".secrets")
ASSIGNMENT_2__SERVICE_1__WORLD_AIR_QUALITY_INDEX_API_KEY = os.getenv("ASSIGNMENT_2__SERVICE_1__WORLD_AIR_QUALITY_INDEX_API_KEY")
#print(ASSIGNMENT_2__SERVICE_1__WORLD_AIR_QUALITY_INDEX_API_KEY)

ASSIGNMENT_2__SERVICE_1__WORLD_AIR_QUALITY_INDEX_API_URL = os.getenv("ASSIGNMENT_2__SERVICE_1__WORLD_AIR_QUALITY_INDEX_API_URL")
#print(ASSIGNMENT_2__SERVICE_1__WORLD_AIR_QUALITY_INDEX_API_URL)

@tool
def get_city_air_quality_summary(city_name:str) -> str:
    """
    The API call is made to https://api.waqi.info/feed/:city/?token=:token
    service to get air quality for given city.
    It takes loaction parameter 'city' and also query parameter 'token'
    Documentation: https://aqicn.org/json-api/doc/.
    The related website for air quality pollution is: https://aqicn.org/
    """    
    response = _get_air_quality_from_service(city_name)
    resp_as_json = response.json() # model_dump_json()
    
    # print(resp_as_json)
    
    try:
        resp_obj = AirQualityResponse.model_validate(resp_as_json)        
        data: AirQualityData = resp_obj.data
        #d = data.get("aqi", "No air quality data found.")
        air_quality_summary_msg = build_air_quality_summary(
            city_name=city_name,
            aqi=data.aqi, #e.g. 61,
            dominant_pollutant=data.dominentpol, #e.g. "pm25",
            iaqi=data.iaqi,                     
            observed_time_iso=data.time.iso, # "2026-02-27T17:00:00-05:00",
        )        
    except:
        d = resp_as_json.get("data") or ""
        if isinstance(d, str):
            air_quality_summary_msg = f"Sorry there was and issue retrieving air quality data for {city_name}. Reason: {d}"
        else:
            air_quality_summary_msg = f"Sorry there was and error retrieving air quality data for {city_name}"

    print(air_quality_summary_msg)

    return air_quality_summary_msg



def _get_air_quality_from_service(city_name: str = 'here'): # -> AirQualityResponse:  
    """
    Fetches air quality data for a given city or current location (when city name is 'here') if no paramter is provided.
    """
    url = ASSIGNMENT_2__SERVICE_1__WORLD_AIR_QUALITY_INDEX_API_URL.format("https://api.waqi.info/feed/{city_name}/", city_name=city_name)
    params = {
        "token": ASSIGNMENT_2__SERVICE_1__WORLD_AIR_QUALITY_INDEX_API_KEY, 
    }

    return requests.get(url, params=params)

