from typing import Dict, Any
import datetime


class AgentService:
    def __init__(self):
        pass

    async def process_question(self, question: str, user: str) -> Dict[str, Any]:
        """Procesa una pregunta del usuario y mantiene el historial de conversación"""
        try:
            return {
                "user": user,
                "question": question,
                "response": "Hola, esta es una respuesta dummy",
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
