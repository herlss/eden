from bs4 import BeautifulSoup
import requests

url = "https://jira-software.status.atlassian.com"
page = requests.get(url)
soup = BeautifulSoup(page.text, "html")

divs = soup.find_all("div", class_="component-container border-color")

for div in divs:
    name = div.find("span", class_="name").text.strip()
    status = div.find("span", class_="component-status").text.strip()