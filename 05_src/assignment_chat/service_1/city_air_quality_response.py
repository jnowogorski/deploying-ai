from __future__ import annotations
from typing import List, Optional
from pydantic import BaseModel, Field


class Attribution(BaseModel):
    url: str = Field(..., description="Attribution URL.")
    name: str = Field(..., description="Attribution name.")
    logo: Optional[str] = Field(None, description="Attribution logo filename (if provided).")



class City(BaseModel):
    name: str = Field(..., description="Name of the monitoring station.")
    geo: List[float] = Field(..., description="Latitude/Longitude of the monitoring station.")
    url: str = Field(..., description="Webpage associated to the monitoring station.")
    location: Optional[str] = Field(None, description="Optional additional location string.")


class AQTime(BaseModel):
    s: str = Field(..., description="Local measurement time.")
    tz: str = Field(..., description="Station timezone.")
    v: Optional[int] = Field(None, description="Unix epoch timestamp (if provided).")
    iso: Optional[str] = Field(None, description="ISO-8601 timestamp (if provided).")


class IAQIValue(BaseModel):
    v: float = Field(..., description="Individual AQI / measurement value.")


class IAQI(BaseModel):   
    """
    Instant / individual values for pollutants and some weather metrics.

    The API exposes pollutants as IAQI (e.g., pm25, pm10, no2, o3, co, so2) and may also include
    meteorological fields such as temperature, humidity, pressure, wind, etc.
    """
    # --- Meteorological / auxiliary fields commonly seen ---
    dew: Optional[IAQIValue] = Field(None, description="Dew point temperature (commonly in °C).")
    h: Optional[IAQIValue] = Field(None, description="Relative humidity (commonly in %).")
    p: Optional[IAQIValue] = Field(None, description="Atmospheric pressure (commonly in hPa).")
    t: Optional[IAQIValue] = Field(None, description="Air temperature (commonly in °C).")
    w: Optional[IAQIValue] = Field(None, description="Wind speed (unit depends on station feed; often m/s).")
    wg: Optional[IAQIValue] = Field(None, description="Wind gust speed (unit depends on station feed; often m/s).")

    # --- Pollutants ---
    pm25: Optional[IAQIValue] = Field(None, description="PM2.5 Individual AQI.")
    pm10: Optional[IAQIValue] = Field(None, description="PM10 Individual AQI.")
    o3: Optional[IAQIValue] = Field(None, description="Ozone (O₃) Individual AQI.")
    no2: Optional[IAQIValue] = Field(None, description="Nitrogen dioxide (NO₂) Individual AQI.")
    so2: Optional[IAQIValue] = Field(None, description="Sulfur dioxide (SO₂) Individual AQI.")
    co: Optional[IAQIValue] = Field(None, description="Carbon monoxide (CO) Individual AQI.")

    model_config = {"extra": "allow"}


# ---------- forecast ----------

class DailyForecastItem(BaseModel):
    avg: float = Field(..., description="Average forecast value for the day.")
    day: str = Field(..., description="Forecast day (YYYY-MM-DD).")
    max: float = Field(..., description="Maximum forecast value for the day.")
    min: float = Field(..., description="Minimum forecast value for the day.")


class DailyForecast(BaseModel):
    pm25: Optional[List[DailyForecastItem]] = Field(None, description="PM2.5 daily forecast.")
    pm10: Optional[List[DailyForecastItem]] = Field(None, description="PM10 daily forecast.")
    o3: Optional[List[DailyForecastItem]] = Field(None, description="Ozone (O3) daily forecast.")
    uvi: Optional[List[DailyForecastItem]] = Field(None, description="Ultra Violet Index (UVI) daily forecast.")

    model_config = {"extra": "allow"}


class Forecast(BaseModel):
    daily: DailyForecast = Field(..., description="Daily forecast data.")


class DebugInfo(BaseModel):
    sync: Optional[str] = Field(None, description="Debug sync timestamp (if provided).")


# ---------- station data (the `data` object) ----------

class AirQualityData(BaseModel):
    idx: int = Field(..., description="Unique ID for the city monitoring station.")
    aqi: int = Field(..., description="Real-time air quality information (AQI).")
    time: AQTime = Field(..., description="Measurement time information.")
    city: City = Field(..., description="Information about the monitoring station.")
    attributions: List[Attribution] = Field(..., description="EPA Attribution for the station.")
    iaqi: IAQI = Field(..., description="Individual AQI / measurements by pollutant.")
    forecast: Optional[Forecast] = Field(None, description="Forecast data (if provided).")

    dominentpol: Optional[str] = Field(None, description="Dominant pollutant (if provided).")
    debug: Optional[DebugInfo] = Field(None, description="Debug info (if provided).")

    model_config = {"extra": "allow"}


# ---------- response ----------
class AirQualityResponse(BaseModel):
    status: str = Field(..., description="Status code, can be 'ok' or 'error'.")
    data: "AirQualityData" = Field(..., description="Station data.")