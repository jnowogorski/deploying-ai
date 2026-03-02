# Assignemnt2 - Service 2: Semantic Query
#
from langchain.tools import tool
import chromadb
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

from dotenv import load_dotenv
from utils.logger import get_logger
from pathlib import Path
import os

_logs = get_logger(__name__)

load_dotenv()
load_dotenv(".env")
load_dotenv(".secrets")

dir = Path(__file__).resolve().parent #.parent
# PERSIST_DIR = "./chroma_db"
PERSIST_DIR = f"{dir}\\data\\chroma_db"
print(PERSIST_DIR)


ASSIGNMENT_2__SERVICE_2__CHROMA_DB_COLLECTION_NAME = os.getenv("ASSIGNMENT_2__SERVICE_2__CHROMA_DB_COLLECTION_NAME")
#print(ASSIGNMENT_2__SERVICE_2__CHROMA_DB_COLLECTION_NAME)

chroma_client = chromadb.PersistentClient(path=PERSIST_DIR)

print("Collections:")
print(chroma_client.list_collections())
# print(os.getenv('API_GATEWAY_KEY'))

collection = chroma_client.get_collection(
	name=ASSIGNMENT_2__SERVICE_2__CHROMA_DB_COLLECTION_NAME,
	embedding_function = OpenAIEmbeddingFunction(
                            api_key = "any value",
                            model_name="text-embedding-3-small",
                            api_base='https://k7uffyg03f.execute-api.us-east-1.amazonaws.com/prod/openai/v1',
                            default_headers={"x-api-key": os.getenv('API_GATEWAY_KEY')}																										
                        )																																									
)



@tool
def answer_air_quality_related_question(query: str, n_results: int = 1) -> list[str]:
    """Searches for answer for air quality related question based on the query. Returns n_results finds."""
    print(f">>>  Looking up info in vectorDB ({query})")
    answers = get_context(query, collection, n_results)
    print(answers)
    print("~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~")
    return answers



def get_context_data(query:str, collection:chromadb.api.models.Collection, top_n:int):
    results = collection.query(
        query_texts=[query],
        n_results=top_n
    )
    context_data = []
    # print("- - - - - - - - - - - - - - -")
    # print(results)
    # print("- - - - - - - - - - - - - - -")
    for idx, custom_id in enumerate(results['ids'][0]):        
        context_data.append(results['documents'][0][idx])
    return context_data



def get_context(query:str, collection:chromadb.api.models.Collection, top_n:int):
    context_data = get_context_data(query, collection, top_n)
    explanations = []
    if not context_data:
        return explanations
    for item in context_data:
        explanations.append(item)
    return explanations