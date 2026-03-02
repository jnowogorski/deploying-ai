from __future__ import annotations
from typing import Optional, Dict, Tuple, List
from assignment_chat.service_1.city_air_quality_response import IAQI

def _aqi_category(aqi: float) -> Tuple[str, str]:
    """US EPA AQI categories (commonly used by AQICN for AQI/IAQI)."""
    if aqi <= 50:
        return "Good", "Air quality is satisfactory; little to no risk."
    if aqi <= 100:
        return "Moderate", "Acceptable; unusually sensitive people may experience symptoms."
    if aqi <= 150:
        return "Unhealthy for Sensitive Groups", "Sensitive groups may be affected; most people are okay."
    if aqi <= 200:
        return "Unhealthy", "Everyone may begin to feel effects; sensitive groups more serious."
    if aqi <= 300:
        return "Very Unhealthy", "Health alert; increased risk for everyone."
    return "Hazardous", "Health warning: everyone may experience serious effects."


def _fmt(value: Optional[float], unit: str, decimals: int = 0) -> Optional[str]:
    if value is None:
        return None
    if decimals <= 0:
        return f"{value:.0f}{unit}"
    return f"{value:.{decimals}f}{unit}"


def build_air_quality_summary(
    *,
    city_name: Optional[str],
    aqi: Optional[int],
    dominant_pollutant: Optional[str],
    iaqi: IAQI,
    observed_time_iso: Optional[str] = None,
) -> str:
    """
    Produce a air quality summary message based on all available IAQI values.
    - Pollutant IAQI values are treated as AQI units.
    - Weather related values use common units.
    """
    lines: List[str] = []
    DIV_LINE_SINGLE = "----------------------------------------------------------"
    DIV_LINE_HEADER = "=========================================================="

    # Header
    place = city_name or "your location"
    time = observed_time_iso or ""
    if aqi is not None:
        cat, hint = _aqi_category(float(aqi))
        dp = f" (dominant: {dominant_pollutant})" if dominant_pollutant else ""        
        lines.append(f"\n\nAir quality in {place} {time}")
        lines.append(f"{DIV_LINE_HEADER}\n")
        lines.append(f"AQI {aqi} — {cat}{dp}.")
        lines.append(hint)
    else:        
        lines.append(f"\n\nAir quality in {place} {time}")
        lines.append(f"{DIV_LINE_HEADER}\n")
        lines.append("I don't have an overall AQI right now, but here are the latest readings:")



    # Build sections from IAQI fields that exist
    # Pollutants (IAQI / AQI units)
    pollutant_specs: List[Tuple[str, str]] = [
        ("pm25", "PM2.5"),
        ("pm10", "PM10"),
        ("o3", "O₃"),
        ("no2", "NO₂"),
        ("so2", "SO₂"),
        ("co", "CO"),
    ]
    pollutant_bits: List[str] = []
    for field, label in pollutant_specs:
        obj = getattr(iaqi, field, None)
        if obj is not None and obj.v is not None:
            cat, _ = _aqi_category(float(obj.v))
            pollutant_bits.append(f" · {label}: {obj.v:.0f} AQI ({cat})\n")
    if pollutant_bits:        
        lines.append(f"\nPollutants (IAQI):\n{DIV_LINE_SINGLE}")
        lines.append("".join(pollutant_bits))

    # Weather/comfort metrics
    t = iaqi.t.v if iaqi.t else None
    dew = iaqi.dew.v if iaqi.dew else None
    rh = iaqi.h.v if iaqi.h else None
    p = iaqi.p.v if iaqi.p else None
    w = iaqi.w.v if iaqi.w else None
    wg = iaqi.wg.v if iaqi.wg else None

    wx_bits: List[str] = []
    if t is not None:
        wx_bits.append(f"Temp: {_fmt(t, '°C', 0)}\n")
    if dew is not None:
        wx_bits.append(f"Dew point: {_fmt(dew, '°C', 0)}\n")
    if rh is not None:
        wx_bits.append(f"Humidity: {_fmt(rh, '%', 0)}\n")
    if p is not None:
        wx_bits.append(f"Pressure: {_fmt(p, ' hPa', 0)}\n")
    if w is not None:
        # AQICN wind unit depends on feed 
        wx_bits.append(f"Wind: {_fmt(w, ' m/s', 0)}\n")
    if wg is not None:
        wx_bits.append(f"Gusts: {_fmt(wg, ' m/s', 1)}\n")

    if wx_bits:
        lines.append(f"Conditions:\n{DIV_LINE_SINGLE}")
        lines.append(" · " + " · ".join(wx_bits))

    # Advice based on dominant pollutant / levels available
    advice: List[str] = []
    # Prefer dominant pollutant if present, otherwise use worst pollutant value we have.
    worst_val = None
    worst_name = None
    for field, label in pollutant_specs:
        obj = getattr(iaqi, field, None)
        if obj is not None:
            if worst_val is None or obj.v > worst_val:
                worst_val = obj.v
                worst_name = label

    if worst_val is not None:
        if worst_val <= 50:
            advice.append("It’s a good time for outdoor activities.\n")
        elif worst_val <= 100:
            advice.append("Most people can be outside as usual.\n")
            advice.append("Very sensitive folks may want to take it easy.\n")
        elif worst_val <= 150:
            advice.append("If you’re sensitive (asthma/allergies/heart-lung issues), consider reducing prolonged outdoor exertion.\n")
        elif worst_val <= 200:
            advice.append("Consider limiting strenuous outdoor activity.\n")
            advice.append("Sensitive groups should take extra care.\n")
        else:
            advice.append("Try to stay indoors with clean air if possible.\n")
            advice.append("Consider a mask if you must be outside.\n")

        if worst_name:
            advice.append(f"Main concern right now is: ** {worst_name} **.\n")

    if advice:
        lines.append(f"Quick guidance:\n{DIV_LINE_SINGLE}")
        lines.append(" · " + " · ".join(advice))

    return "\n".join(lines)