from app.scraping.atlassian import AtlassianStatus, JiraStatus

class ScrapingService:
    @classmethod
    def getJiraStatus(self):
        atlassianStatus = AtlassianStatus()
        jiraStatus = JiraStatus()

        if jiraStatus:
            return jiraStatus
        else:
            return atlassianStatus