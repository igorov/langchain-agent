from fastapi import HTTPException
from typing import Dict, Any
from src.agent.agent import AgentService
from src.entities.agent_entities import AgentRequest

class AgentController:
    
    def __init__(self):
        self.agent_service = AgentService()
    
    async def process_agent_request(self, request: AgentRequest) -> Dict[str, Any]:
        try:
            return await self.agent_service.process_question(
                question=request.question,
                user=request.user
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error processing request: {str(e)}")
