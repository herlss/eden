from app.scraping.atlassian import AtlassianIncidents, JiraStatus
from app.scraping.aws import AwsDashboardData

class DashboardService:
    @classmethod
    def getAwsDashboard(self):
        dashboard = {}

        data = AwsDashboardData()

        filter = [incident for incident in data if incident["region_name"] in ["N. Virginia", "Sao Paulo"]]

        serviceCount = {}
        for incident in filter:
            serviceName = incident["service_name"]
            serviceCount[serviceName] = serviceCount.get(serviceName, 0) + 1

        saoPauloCount = sum(1 for incident in filter if incident["region_name"] == "Sao Paulo")
        virginiaCount = sum(1 for incident in filter if incident["region_name"] == "N. Virginia")

        regions = [
            ["Sao Paulo", saoPauloCount],
            ["N. Virginia", virginiaCount]
        ]

        dashboard["Incidents by Service"] = [[serviceName, count] for serviceName, count in serviceCount.items()]
        dashboard["Incidents by Region"] = regions
        dashboard["Total Incidents"] = len(filter)

        return dashboard
    
    @classmethod
    def getJiraDashboard(cls):
        dashboard = {}

        jiraServerHealth = cls.getJiraServerHealth()
        if jiraServerHealth:
            dashboard["Jira Server Health"] = jiraServerHealth

        dashboard["History of the Last Fifty Incidents"] = cls.getJiraHistoricIncidents()

        return dashboard
    
    def getJiraServerHealth():
        serverHealth = {}
        data = JiraStatus()
        if data:
            for server in data:
                if server[1] in serverHealth:
                    serverHealth[server[1]][0].append(server[0])
                    serverHealth[server[1]][1] += 1
                else:
                    serverHealth[server[1]] = [[server[0]], 1]
            return serverHealth
        else:
            return None
    
    def getJiraHistoricIncidents():
        serverHistoric = {}
        data = AtlassianIncidents()['incidents']
        filter = [incident for incident in data if "Jira" in incident['name']]
        for incidents in filter:
            if incidents['impact'] in serverHistoric:
                serverHistoric[incidents['impact']][0] += 1
                if incidents['status'] == "resolved":
                    serverHistoric[incidents['impact']][1] += 1
            else:
                serverHistoric[incidents['impact']] = [1, 0]
                if incidents['status'] == "resolved":
                    serverHistoric[incidents['impact']][1] = 1
        
        return serverHistoric