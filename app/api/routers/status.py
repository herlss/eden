from app.api.sevices.scraping import ScrapingService
from fastapi import APIRouter

router = APIRouter()

@router.get('/')
async def test():
    return 'whatever'

@router.get('/aws')
async def getAwsStatus():
    print(f'function that will return AWS status page')

@router.get('/jira')
async def getJiraStatus():
    print(f'function that will return Jira status page')
    return ScrapingService.getJiraStatus()

@router.get('/oci')
async def getOciStatus():
    print(f'function that will return OCI status page')