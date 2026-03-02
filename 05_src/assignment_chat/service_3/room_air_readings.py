from pydantic import BaseModel, Field

class RoomAirReadings(BaseModel):
    """Structured air measurements response."""
    room: str = Field(..., description="Room name.")
    temperature: float = Field(..., description="The current temperature in Celsius.")
    humidity: float = Field(..., description="The current humidity level as a percentage.")  