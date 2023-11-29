from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def test():
    return 'whatever'


@router.get('/aws')
def getAwsStatus():
    return f'function that will return AWS status page'

@router.get('/jira')
def getJiraStatus():
    return f'function that will return Jira status page'

@router.get('/oci')
def getOciStatus():
    return f'function that will return OCI status page'