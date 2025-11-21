from typing import Dict, Any
import datetime
import os
from langchain_openai import ChatOpenAI
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from langchain_openai import OpenAIEmbeddings
from src.agent.tools import get_tools
from langchain.agents import create_agent
from langchain.messages import SystemMessage, HumanMessage, AIMessage

class AgentService:
    def __init__(self):
        model = "gpt-4o-mini"
        system_prompt = "Eres un asistente util"
        llm_model = self.init_model(model)
        self.qdrant_store = self.init_qdrant()
        self.agent = self.init_agent(system_prompt, llm_model)

    async def process_question(self, question: str, user: str) -> Dict[str, Any]:
        """Procesa una pregunta del usuario y mantiene el historial de conversación"""
        # Use with chat models
        messages = []
        messages.append(HumanMessage(question))

        result = self.agent.invoke(
            {"messages": messages}
        )

        print(result["messages"][-1].content)
        try:
            return {
                "user": user,
                "question": question,
                "response": result["messages"][-1].content,
                "timestamp": datetime.datetime.now().isoformat(),
                "status": "success"
            }
            
        except Exception as e:
            return {
                "user": user,
                "question": question,
                "response": f"Error al procesar la pregunta: {str(e)}",
                "timestamp": datetime.datetime.now().isoformat(),
                "status": "error"
            }

    def init_model(self, model: str):
        return ChatOpenAI(
            base_url="https://api.openai.com/v1",
            openai_proxy=None,
            model = model,
            stream_usage=True,
            streaming=True,
            api_key = os.getenv("OPENAI_API_KEY")
        )

    def init_qdrant(self):
        # Cargar credenciales desde variables de entorno
        qdrant_url = os.getenv("QDRANT_URL")
        qdrant_key = os.getenv("QDRANT_API_KEY")
        collection_name = os.getenv("QDRANT_COLLECTION_NAME", "academy")

        # Configure embeddings (usa el mismo modelo que el notebook de ingesta)
        embeddings_model = "text-embedding-3-small"
        embeddings = OpenAIEmbeddings(model=embeddings_model)

        client = QdrantClient(
            url=qdrant_url,
            api_key=qdrant_key
        )

        # Crear el vector store en Qdrant
        return QdrantVectorStore(
            client=client,
            collection_name=collection_name,
            embedding=embeddings
        )

    def init_agent(self, system_prompt: str, llm_model: ChatOpenAI):
        return create_agent(
            model = llm_model,
            system_prompt = system_prompt,
            tools = self.init_tools()
        )

    def init_tools(self):
        return get_tools(self.qdrant_store)
