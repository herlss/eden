from app.api.services.status import StatusService
from fastapi import APIRouter

router = APIRouter(prefix="/status")

@router.get('/jira')
async def getJiraStatus():
    return StatusService.getJiraStatus()