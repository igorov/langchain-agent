from datetime import datetime
from langchain_core.tools import tool

def create_retrieve_context_tool(qdrant_store):
    """Factory function para crear la tool retrieve_context con acceso a qdrant_store"""
    @tool(response_format="content_and_artifact")
    def retrieve_context(query: str):
        """Recupera informacion para ayudar a responder informacion sobre matriculas."""
        retrieved_docs = qdrant_store.similarity_search(query, k=5)
        serialized = "\n\n".join(
            (f"Source: {doc.metadata}\nContent: {doc.page_content}")
            for doc in retrieved_docs
        )
        return serialized, retrieved_docs
    return retrieve_context

@tool
def get_weather(location: str) -> str:
    """Get weather information for a location."""
    return f"Weather in {location}: Sunny, 72°F"

@tool
def sumar(a: int, b: int) -> int:
  """
  Dados dos parametros a y b, devuelve la suma de ambos

  @param a: primer numero
  @param b: segundo numero
  @return: la suma de a y b
  """
  print(f"sumando a: {a} con b: {b}")
  return a + b

@tool
def multiplicar(a: int, b: int) -> int:
  """
  Dados dos parametros a y b, devuelve la multiplicacion de ambos
  @param a: primer numero
  @param b: segundo numero
  @return: la multiplicacion de a y b
  """
  print(f"multiplicando a: {a} con b: {b}")
  return a * b

@tool
def restar(a: int, b: int) -> int:
  """
  Dads dos parametros a y b, devuelve la resta de ambos
  @param a: primer numero
  @param b: segundo numero
  @return: la resta de a y b
  """
  print(f"restando a: {a} con b: {b}")
  return a - b

@tool
def get_current_date() -> dict:
    """
    Obtener la fecha actual en el formato YYYY-MM-DD
    """
    return {"current_date": datetime.now().strftime("%Y-%m-%d")}

# Tools estáticas (no necesitan dependencias)
static_tools = [get_weather, sumar, multiplicar, restar, get_current_date]

def get_tools(qdrant_store):
    """Retorna todas las tools, incluyendo las que necesitan dependencias"""
    retrieve_context = create_retrieve_context_tool(qdrant_store)
    return static_tools + [retrieve_context]