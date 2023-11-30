from app.scraping.atlassian import AtlassianIncidents, JiraStatus
from app.scraping.aws import AwsDashboardData
from datetime import datetime
import requests as req
import json as js

from app.scraping.oci import OciStatus

class DashboardService:
    @classmethod
    def getAwsDashboard(self):
        data = AwsDashboardData()

        if data:
            dashboard = {}

            filter = [incident for incident in data if incident["region_name"] in ["N. Virginia", "Sao Paulo"]]

            years = {}
            for incident in filter:
                timestamp = incident["launch_date"]
                dt_object = datetime.fromtimestamp(timestamp)
                year = str(dt_object.year)
                
                if year in years.keys():
                    years[year] += 1
                else:
                    years[year] = 1
            
            sp_count = sum(1 for incident in filter if incident["region_name"] == "Sao Paulo")
            virginia_count = sum(1 for incident in filter if incident["region_name"] == "N. Virginia")

            regions = [
                ["Sao Paulo", sp_count],
                ["N. Virginia", virginia_count]
            ]

            dashboard["Incidents by Region"] = regions
            dashboard["Total Incidents"] = len(filter)
            dashboard["Incidents By Year"]

            return dashboard
        else:
            return {"Notification": "Error fetching AWS"}
    
    @classmethod
    def getJiraDashboard(cls):

        jiraHistoricIncidents = cls.getJiraHistoricIncidents()

        if jiraHistoricIncidents:
            jiraServerHealth = cls.getJiraServerHealth()

            dashboard = {}
            if jiraServerHealth:
                dashboard["Jira Server Health"] = jiraServerHealth

            dashboard["History of the Last Fifty Incidents"] = jiraHistoricIncidents
            return dashboard
        else:
            return {"Notification": "Error fetching Atlassian"}
    
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
        
        data = AtlassianIncidents()

        if data:
            data = data['incidents']
            serverHistoric = {}
            totalIncidents = 0
            totalIncidentsResolved = 0
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
        else:
            return {"Notification": "Error fetching Atlassian"}

    # Gráfico do dash abaixo será apenas 1(ou 2) big numbers. Colocar na descrição do(s) big number(s): "Oracle Services in Normal 
    # Performance status" e "Oracle Services in not Normal Performance status :/"
    @classmethod
    def getOciDashboard(cls):

        data = OciStatus()

        if data:
            dashboard = []

            for region in data["regionHealthReports"]:
                if "Sao Paulo" in region["regionName"]:
                    dashboard.append(region)
                elif "Vinhedo" in region["regionName"]:
                    dashboard.append(region)

            totalOn = 0
            totalOff = 0

            for region in dashboard:
                for service in region["serviceHealthReports"]:
                    if service["serviceStatus"] == "NormalPerformance":
                        totalOn += 1
                    else:
                        totalOff += 1

            return {"Normal Performance services": totalOn, "Not Normal Performance services": totalOff}
        else:
            return {"Notification": "Error fetching OCI"}
