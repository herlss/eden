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
        
    @classmethod
    def getAwsStatus(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        browser = webdriver.Chrome(options=chrome_options)
        url = "https://health.aws.amazon.com/health/status"
        browser.get(url)

        btn = browser.find_element(By.CLASS_NAME, "awsui_tabs-tab_14rmt_g3ojk_227")
        btn.click()

        time.sleep(1)

        html_source = browser.page_source  
        page = BeautifulSoup(html_source, "html.parser")
        for data in page(['style', 'script']):
            data.decompose()
        data_out='     '.join(page.stripped_strings).replace("\xa0", " ")
        print(page.prettify)
        return [data_out]