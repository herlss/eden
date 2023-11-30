from app.scraping.atlassian import AtlassianIncidents, JiraStatus
from app.scraping.aws import AwsDashboardData
import requests as req
import json as js

from app.scraping.oci import OciStatus

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
        serverHealth = {
            'Operational': 0,
            'Outage': 0
        }
        data = JiraStatus()
        if data:
            for server in data:
                if server[1] == 'Operational':
                    serverHealth['Operational'] += 1
                else:
                    serverHealth['Outage'] += 1
            return serverHealth
        else:
            return None
    
    def getJiraHistoricIncidents():
        serverHistoric = {}
        totalIncidents = 0
        totalIncidentsResolved = 0
        data = AtlassianIncidents()['incidents']
        filter = [incident for incident in data if "Jira" in incident['name']]
        for incidents in filter:
            if incidents['impact'] in serverHistoric:
                serverHistoric[incidents['impact']][0] += 1
                totalIncidents += 1
                totalIncidentsResolved += 1
                if incidents['status'] == "resolved":
                    serverHistoric[incidents['impact']][1] += 1
            else:
                serverHistoric[incidents['impact']] = [1, 0]
                totalIncidents += 1
                totalIncidentsResolved += 1
                if incidents['status'] == "resolved":
                    serverHistoric[incidents['impact']][1] = 1

        serverHistoric['Total of Incidents'] = totalIncidents
        serverHistoric['Total of Incidents Resolved'] = totalIncidentsResolved
        return serverHistoric

    # Gráfico do dash abaixo será apenas 1(ou 2) big numbers. Colocar na descrição do(s) big number(s): "Oracle Services in Normal 
    # Performance status" e "Oracle Services in not Normal Performance status :/"
    @classmethod
    def getOciDashboard(cls):

        data = OciStatus()
        json = []

        for region in data["regionHealthReports"]:
            if "Sao Paulo" in region["regionName"]:
                json.append(region)
            elif "Vinhedo" in region["regionName"]:
                json.append(region)

        totalOn = 0
        totalOff = 0

        for region in json:
            for service in region["serviceHealthReports"]:
                if service["serviceStatus"] == "NormalPerformance":
                    totalOn += 1
                else:
                    totalOff += 1

        return {"Normal Performance services": totalOn, "Not Normal Performance services": totalOff}
