import requests
from bs4 import BeautifulSoup

def AtlassianStatus():
    url = "https://status.atlassian.com/api/v2/status.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Atlassian status: {e}")
        return None
        
def AtlassianIncidents():
    url = "https://status.atlassian.com/api/v2/incidents.json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Atlassian status: {e}")
        return None

def JiraStatus():
    url = "https://jira-software.status.atlassian.com"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        divs = soup.find_all("div", class_="component-container border-color")
        return [(div.find("span", class_="name").text.strip(),
                div.find("span", class_="component-status").text.strip())
                for div in divs]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Jira status: {e}")
        return []