import requests

def AwsDashboardData():
        url = "https://di1pzre3hzbi4.cloudfront.net/services.json"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.RequestException as e:
            print(f"Error fetching AWS data: {e}")
            return None