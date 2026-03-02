# Assignemnt2 - Service 3: Air measurements readings in the house/room
import asyncio
from fastmcp import Client
from langchain.tools import tool
from dotenv import load_dotenv
from assignment_chat.service_3.room_air_readings import RoomAirReadings
import os

from utils.logger import get_logger
_logs = get_logger(__name__)

load_dotenv()

mcp_url = os.getenv("ASSIGNMENT_2__SERVICE_3__MCP_CLIENT_URL")
# _logs.info(f'Using MCP URL: {mcp_url}')
print(f'Using MCP URL: {mcp_url}')

import asyncio
from fastmcp import Client    

mcp_client = Client(mcp_url)

@tool(description="Fetch recent in-house air measurements for a given room (e.g., 'kitchen', 'bedroom').")
async def get_air_measurements_in_room(room: str) -> RoomAirReadings:
    async with mcp_client:
        # Basic server interaction
        await mcp_client.ping()
        
        # List available operations
        # available_tools = await mcp_client.list_tools()
        # _logs.info(f'Available tools: {available_tools}')
        # resources = await mcp_client.list_resources()
        # _logs.info(f'Available resources: {resources}')
        # prompts = await mcp_client.list_prompts()
        # _logs.info(f'Available prompts: {prompts}')

        # Execute operations
        result = await mcp_client.call_tool("air_measurements_in_room_service", {"room": room})
        print("- - - - - - - - - - - - - - -")
        print(result)
        print("- - - - - - - - - - - - - - -")
        # _logs.info(result)

        return result  # RoomAirReadings.model_validate(result)
        # return RoomAirReadings.model_validate(result) #Pydantic
        # return RoomAirReadings.model_validate(result).model_dump()
    


# if __name__ == "__main__":
#     asyncio.run(get_air_measurements_in_house_service("living_room"))