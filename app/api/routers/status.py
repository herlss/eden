from app.api.services.scraping import ScrapingService
from fastapi import APIRouter

router = APIRouter(prefix="/status")

@router.get('/aws')
async def getAwsStatus():
    return ScrapingService.getAwsStatus()

@router.get('/jira')
async def getJiraStatus():
    return ScrapingService.getJiraStatus()