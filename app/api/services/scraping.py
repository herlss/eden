from app.scraping.atlassian import AtlassianStatus, JiraStatus
from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

class ScrapingService:
    @classmethod
    def getJiraStatus(self):
        atlassianStatus = AtlassianStatus()
        jiraStatus = JiraStatus()

        if jiraStatus:
            return jiraStatus
        else:
            return atlassianStatus.get('status').get('description')