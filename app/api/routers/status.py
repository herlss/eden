from app.api.services.scraping import ScrapingService
from fastapi import APIRouter

router = APIRouter(prefix="/status")

@router.get('/aws')
async def getAwsStatus():
    print(f'function that will return AWS status page')

@router.get('/jira')
async def getJiraStatus():
    return ScrapingService.getJiraStatus()

@router.get('/oci')
async def getOciStatus():
    print(f'function that will return OCI status page')