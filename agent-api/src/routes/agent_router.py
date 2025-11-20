from fastapi import APIRouter
from src.controller.agent_controller import AgentController
from src.entities.agent_entities import AgentRequest

router = APIRouter(prefix="/api", tags=["agent"])

# Crear una instancia del controlador
agent_controller = AgentController()

@router.post("/agent", summary="Process agent question")
async def agent_endpoint(request: AgentRequest):
    return await agent_controller.process_agent_request(request)
