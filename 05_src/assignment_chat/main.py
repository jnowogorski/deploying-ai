
from langgraph.graph import StateGraph, MessagesState, START
from langchain.chat_models import init_chat_model
from langgraph.prebuilt.tool_node import ToolNode, tools_condition
from langchain_core.messages import SystemMessage,  HumanMessage

from assignment_chat.prompts import return_instructions
from assignment_chat.service_1.tool_city_air_quality import get_city_air_quality_summary
from assignment_chat.service_2.tool_answer_air_quality_related_questions import answer_air_quality_related_question
from assignment_chat.service_3.tool_air_measurements_in_room import get_air_measurements_in_room

from dotenv import load_dotenv
import os

from utils.logger import get_logger


_logs = get_logger(__name__)
load_dotenv(".env")
load_dotenv(".secrets")
open_ai_model = os.getenv("ASSIGNMENT_2__OPENAI_MODEL", "gpt-4")
print(f"Using model: {open_ai_model}")

chat_agent = init_chat_model(
    f"openai:{open_ai_model}",
    base_url='https://k7uffyg03f.execute-api.us-east-1.amazonaws.com/prod/openai/v1', 
    api_key='any value',
    default_headers={"x-api-key": os.getenv('API_GATEWAY_KEY')}
)

tools = [get_city_air_quality_summary, answer_air_quality_related_question, get_air_measurements_in_room]

instructions = return_instructions()



async def call_model(state: MessagesState):
    """LLM decides whether to call a tool or not"""
    # response = await chat_agent.bind_tools(tools).invoke( 
    response = await chat_agent.bind_tools(tools).ainvoke( 
        [SystemMessage(content=instructions)] + state["messages"]
    )
    return {"messages": [response]}

def get_graph():
    
    builder = StateGraph(MessagesState)
    builder.add_node(call_model)
    builder.add_node(ToolNode(tools))
    builder.add_edge(START, "call_model")
    builder.add_conditional_edges(
        "call_model",
        tools_condition,
    )
    builder.add_edge("tools", "call_model")
    graph = builder.compile()
    return graph
