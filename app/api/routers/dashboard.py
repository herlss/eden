from app.api.services.scraping import ScrapingService
from fastapi import APIRouter

router = APIRouter(prefix="/dashboard")

@router.get('/aws')
async def getAwsDash():
    return "Aws Dash"

@router.get('/jira')
async def getJiraDash():
    return "Jira Dash"

@router.get('/oci')
async def getOciDash():
    return "OCI Dash"