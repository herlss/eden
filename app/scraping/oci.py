import requests

def OciStatus():
    url = "https://ocistatus.oraclecloud.com/api/v2/components_v2.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching OCI status: {e}")
        return None