# Assignemnt2 - MCP Server that provides air measurement readings (temperature, humidity) in the house
import random
from fastmcp import FastMCP
from utils.logger import get_logger
from dotenv import load_dotenv
import ngrok
import os
from assignment_chat.service_3.room_air_readings import RoomAirReadings

# Load environment variables and secrets
load_dotenv()
load_dotenv(".secrets")

# Setup Logger
_logs = get_logger(__name__)


MCP_DOMAIN = os.getenv("ASSIGNMENT_2__SERVICE_3__MCP_SERVER_DOMAIN")


mcp = FastMCP(
    name="air_measurements_in_room_service",
    instructions="""
    This server provides air conditions in the house.
    Responds with structured data including room, temperature and humidity.
    """
)



@mcp.tool(
        name="air_measurements_in_room_service",
        description="Provides room air measurement readings.",
)
def air_measurements_in_room_service(room: str) -> RoomAirReadings:
    """Fetches air data from room sensors in the house."""
    # Simulated data:  
    random_temp_delta = 5 * random.random()
    random_hum_delta = 15 * random.random()
    return RoomAirReadings(room=room, temperature=19 + random_temp_delta, humidity=45.0 + random_hum_delta)


# if __name__ == "__main__":
#     mcp.run(
#         transport="http",
#         host="localhost", 
#         port=3000, 
#     )

if __name__ == "__main__":
    listener = ngrok.forward("localhost:3000", authtoken_from_env=True,
                                domain=MCP_DOMAIN)
    _logs.info(f'Ngrok tunnel established at {listener.url()}')
    mcp.run(
        transport="http",
        host="localhost", 
        port=3000, 
    )
