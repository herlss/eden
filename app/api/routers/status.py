from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def test():
    return 'whatever'


@router.get('/aws/{loc}')
def getAwsStatus(loc):
    return f'function that will return AWS status page on {loc}'

@router.get('/jira/{loc}')
def getJiraStatus(loc):
    return f'function that will return Jira status page on {loc}'

@router.get('/oci/{loc}')
def getOciStatus(loc):
    return f'function that will return OCI status page on {loc}'