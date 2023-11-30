from app.api.services.dashboard import DashboardService
from fastapi import APIRouter

router = APIRouter(prefix="/dashboard")

@router.get('/aws')
async def getAwsDash():
    return DashboardService.getAwsDashboard()

@router.get('/jira')
async def getJiraDash():
    return "Jira Dash"

@router.get('/oci')
async def getOciDash():
    return "OCI Dash"